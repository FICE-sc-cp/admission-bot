from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_info_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="🆘 Допомога", url="https://t.me/fiot_help_bot")

    return builder.as_markup()
