from asyncpg import UniqueViolationError
from loguru import logger

from utils.db_api.db_gino import db
from utils.db_api.shemas.users import Users


async def add_user(user_id: int, tg_first_name: str, tg_last_name: str, name: str, card_number: str, phone_number: str,
                   status: str, bonus: float, number_ie: int, sms_status: bool):
    try:
        user = Users(user_id=user_id, tg_first_name=tg_first_name, tg_last_name=tg_last_name,
                     name=name, card_number=card_number, phone_number=phone_number,
                     status=status, bonus=bonus, number_ie=number_ie, sms_status=sms_status)
        await user.create()
    except UniqueViolationError:
        logger.exception('Ошибка при добавлении пользователя')


async def select_user(user_id):
    """ Выбрать пользователя"""
    try:
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        return user
    except Exception as e:
        logger.exception(f'Ошибка при выборе пользователя: {e}')
