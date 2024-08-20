""" Отчеты по покупкам """

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove
from datetime import datetime
from keyboards.default import kb_report, kb_report_cancel, cancel_registration, cancel_change
from loader import dp
from parser.parser import get_parsing
from utils.db_api.ie_commands import get_report_time, get_report_state, update_report_state, get_user_email, \
    get_user_password, update_report_time
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import re


class Report(StatesGroup):
    report_time = State()


@dp.message_handler(Command('setting_report'))
async def setting_report(message: types.Message):
    # смотрим подключены ли отчеты
    if await get_report_state(message.from_user.id):
        await message.answer('Выберите, что хотите изменить:', reply_markup=kb_report_cancel)
    else:
        await message.answer('Подключить ежедневные отчеты по сумме и количеству проданных товаров?',
                             reply_markup=kb_report)


@dp.message_handler(text='Отключить отчеты')
async def disable_reports(message: types.Message):
    await update_report_state(message.from_user.id, False)
    await message.answer('Отчеты отключены', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text='Настроить время отчета')
async def disable_reports(message: types.Message):
    report_time = await get_report_time(message.from_user.id)
    await message.answer(f'Установлено время <b>{report_time}</b>\n'
                         f'Введите новое время отчета в формате: 20:00', reply_markup=cancel_change)
    await Report.report_time.set()


@dp.message_handler(state=Report.report_time)
async def get_number(message: types.Message, state: FSMContext):
    report_time = message.text
    if report_time.lower() == "отменить":
        await state.finish()
        await message.answer('Отменено')
        await state.finish()
    else:
        # Проверка правильности формата времени
        if re.match(r'^([01]\d|2[0-3]):[0-5]\d$', report_time):
            await update_report_time(message.from_user.id, report_time)
            await message.answer(f'Включены ежедневные отчеты в {report_time}', reply_markup=ReplyKeyboardRemove())
            await state.finish()
        else:
            await message.answer('Неверный формат времени. Введите время в формате 24 часа, например, 20:00.',
                                 reply_markup=cancel_change)




@dp.message_handler(text='Отмена')
async def cancel(message: types.Message):
    await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text='Да')
async def connect_reports(message: types.Message):
    await update_report_state(message.from_user.id, True)
    await message.answer('Введите время отчета в формате: 20:00', reply_markup=cancel_change)
    await Report.report_time.set()


@dp.message_handler(Command('report'))
async def send_report(message: types.Message):
    user = message.from_user.id
    login = await get_user_email(user)
    password = await get_user_password(user)
    current_date = datetime.now().strftime("%d.%m.%Y")
    report = await get_parsing(login, password, current_date)
    await message.answer(f'<i>Отчет по продажам:</i>')
    await message.answer(report)




