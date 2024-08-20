import qrcode

from utils.db_api.ie_commands import get_bot_name


async def create_qr_code(user_number):
    bot_name = await get_bot_name(user_number)
    url = f'{bot_name}?start={user_number}'

    return qrcode.make(url)
