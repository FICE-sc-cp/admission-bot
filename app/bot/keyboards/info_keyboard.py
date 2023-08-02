from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_info_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="ℹ️ Інформація",
                   url="https://telegra.ph/%D0%86nformac%D1%96ya-pro-elektronnu-chergu-pri-vstup%D1%96-na-F%D0%86OT-cherez-Telegram-bot-fiot-queue-bot-08-26")
    builder.button(text="🆘 Допомога", url="https://t.me/fiot_help_bot")

    return builder.as_markup()
