""" Регистрация нового автомата """

import re
from aiogram import types
from aiogram.dispatcher import FSMContext
from filters import IsPrivate
from handlers.users.my_qrcode import send_qr_code
from keyboards.default import cancel_registration
from loader import dp
from parser.verification import main_authorize
from states import Registration
from utils.db_api.ie_commands import change_email_and_password, update_bot_name, get_bot_name
from utils.notify_admins import send_admins


@dp.message_handler(text='Отменить регистрацию', state=[Registration.email, Registration.password,
                                                        Registration.number_machines, Registration.name_machines,
                                                        Registration.time_update, Registration.report_time])
async def cast(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Регистрация отменена')


@dp.message_handler(text=['Регистрация', '/register'])
async def register(message: types.Message):
    await message.answer('Для начала работы введите ссылку на своего бота, где будут получать уведомления пользователи'
                         '(например: https://t.me/Kofelevs_bonuses_bot\n'
                         'Если у Вас нет бота, то зарегистрируйте его в https://t.me/BotFather')
    await message.answer('Введите ссылку на бота:', reply_markup=cancel_registration)
    await Registration.bot_name.set()


def validate_telegram_url(url):
    pattern = r'^https://t\.me/[\w_]+$'
    return re.match(pattern, url) is not None


@dp.message_handler(IsPrivate(), state=Registration.bot_name)
async def get_bot(message: types.Message, state: FSMContext):
    url = message.text
    if validate_telegram_url(url):  # Проверяем введенный url
        await update_bot_name(user_id=message.from_user.id, bot_name_new=url)

        await message.answer('Дла продолжения работы введите email и password для сайта https://p.vendista.ru//\n')
        await message.answer('email:', reply_markup=cancel_registration)
        await Registration.email.set()
    else:
        await message.answer('Некорректное имя бота. Пожалуйста, повторите ввод в формате '
                             'https://t.me/Kofelevs_bonuses_bot:',
                             reply_markup=cancel_registration)


@dp.message_handler(IsPrivate(), state=Registration.email)
async def get_email(message: types.Message, state: FSMContext):
    email = message.text
    if validate_email(email):  # Проверяем введенный email
        await state.update_data(email=email)

        await message.answer('пароль:', reply_markup=cancel_registration)
        await Registration.password.set()
    else:
        await message.answer('Некорректный email. Пожалуйста, повторите ввод email:',
                             reply_markup=cancel_registration)


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


@dp.message_handler(state=Registration.password)
async def get_password(message: types.Message, state: FSMContext):
    # Сохранение пароля в состояние
    password = message.text

    data = await state.get_data()
    email = data.get('email')

    # Проверка пароля
    if await main_authorize(email, password):
        await message.answer('Поздравляю! Регистрация прошла успешно!')
        # Сохранение данных в базу данных
        await change_email_and_password(user_id=int(message.from_user.id), new_email=email,
                                        new_password=password
                                        )
        bot_name = await get_bot_name(message.from_user.id)
        await message.answer(
            f'Ваш QR Code для пользователей, его можно распечатать и повесить на Ваши кофеаппараты!\n\n'
            f'Бонусы будут показаны в боте {bot_name}?start={message.from_user.id}')
        await send_qr_code(message.from_user.id)
        await send_admins(dp, f'Новая регистрация - {message.from_user.id}\n'
                              f' @{message.from_user.username}')
        # await message.answer(f'Хотите подключить СМС уведомления для пользователей? (стоимость одной СМС 5 рублей) \n'
        #                      f'Для подключения СМС информирования нажмите /sms_notifications')

        await state.finish()
    else:
        await message.answer('Неверный пароль. Пожалуйста, повторите ввод пароля:',
                             reply_markup=cancel_registration)
