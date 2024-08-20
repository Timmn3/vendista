""" QR Code """

from aiogram import types
from aiogram.dispatcher.filters import Command
from handlers.users.my_qrcode import send_qr_code
from loader import dp
from utils.db_api.ie_commands import get_bot_name

from utils.notify_admins import send_admins


@dp.message_handler(Command('qr_code'))
async def qr_code(message: types.Message):
    bot_name = await get_bot_name(message.from_user.id)
    await message.answer(f'Ваш QR Code для пользователей, его можно распечатать и повесить на Ваши кофеаппараты!\n\n'
                         f'Бонусы будут показаны в боте {bot_name}?start={message.from_user.id}')
    await send_qr_code(message.from_user.id)
    await send_admins(dp, f'Новая регистрация - {message.from_user.id}\n'
                          f' @{message.from_user.username}')
