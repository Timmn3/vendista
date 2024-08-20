from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove

from keyboards.default import kb_sms_cancel, kb_sms
from loader import dp
from utils.db_api.ie_commands import get_sms_status_ie, update_sms_status


@dp.message_handler(Command('sms_notifications'))
async def sms_notifications(message: types.Message):
    # смотрим подключена ли СМС уведомление в кофейне
    if await get_sms_status_ie(message.from_user.id):
        await message.answer('Отключить СМС уведомления для пользователей?', reply_markup=kb_sms_cancel)
    else:
        await message.answer('Подключить СМС уведомления для пользователей? (стоимость одной СМС 5 рублей)',
                             reply_markup=kb_sms)


@dp.message_handler(text='Отключить уведомления')
async def disable_notifications(message: types.Message):
    await update_sms_status(message.from_user.id, False)
    await message.answer('СМС информирование отключено, теперь пользователи будут получать уведомления о балансе '
                         'бонусов только в telegram боте!📲', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text='Отмена')
async def cancel(message: types.Message):
    await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text='да')
async def disable_notifications(message: types.Message):
    await update_sms_status(message.from_user.id, True)
    await message.answer('СМС информирование подключено, теперь пользователи будут получать уведомления о балансе '
                         'бонусов по СМС и в telegram боте!📲', reply_markup=ReplyKeyboardRemove())
