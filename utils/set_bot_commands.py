from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Старт'),
        types.BotCommand('register', 'Регистрация'),
        types.BotCommand('qr_code', 'Ваш QR code'),
        # types.BotCommand('sms_notifications', 'СМС уведомления'),
        types.BotCommand('report', 'Показать отчет'),
        types.BotCommand('setting_report', 'Настройка отчета'),
        types.BotCommand('help', 'Помощь'),

    ])
