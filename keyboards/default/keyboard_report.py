from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_report = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да"),
            KeyboardButton(text="Отмена"),

        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True

)


kb_report_cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отключить отчеты"),
            KeyboardButton(text="Настроить время отчета"),
            KeyboardButton(text="Отмена"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)