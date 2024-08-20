from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from filters import IsPrivate
from keyboards.default import kb_register_machine
from loader import dp
from utils.db_api import ie_commands
from utils.misc import rate_limit
from utils.notify_admins import new_user_registration


@dp.message_handler(IsPrivate(), CommandStart())  # создаем message, который ловит команду /start
async def command_start(message: types.Message):  # создаем асинхронную функцию
    try:
        user = await ie_commands.select_user(message.from_user.id)
        if user.status == 'active':
            await message.answer(f'Привет {user.tg_first_name}!\n')
        else:
            await message.answer(f'Здравствуйте, {user.tg_first_name}!\n'
                                 f'Пожалуйста, пройдите регистрацию'
                                 , reply_markup=kb_register_machine)
    except Exception:
        await ie_commands.add_ie(user_id=message.from_user.id,
                                 tg_first_name=message.from_user.first_name,
                                 tg_last_name=message.from_user.last_name,
                                 name=message.from_user.username,
                                 email='',
                                 password='',
                                 time_update=60,
                                 last_time='20.12.2023 18:08:06',
                                 status='active',
                                 is_run=False,
                                 balance=15,
                                 number_ie=0,
                                 sms_status=False,
                                 bill_id='',
                                 report_time='21:00',
                                 report_state=False,
                                 bot_name='https://t.me/Kofelevs_bonuses_bot',
                                 token='')

        await message.answer(f'Добро пожаловать, {message.from_user.first_name}!\n', reply_markup=kb_register_machine)
        # отправляем админам нового пользователя
        await new_user_registration(dp=dp, user_id=message.from_user.id, first_name=message.from_user.first_name,
                                    username=message.from_user.username)


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text="/my_id")  # создаем message, который ловит команду /id
async def get_unban(message: types.Message):  # создаем асинхронную функцию
    user = await ie_commands.select_user(message.from_user.id)
    await message.answer(f'Ваш id - {user.user_id}')
