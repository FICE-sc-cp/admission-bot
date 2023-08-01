from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.select_confirm import SelectConfirm
from app.types.confirms import Confirms


def get_confirm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for confirm in Confirms:
        builder.button(text=confirm, callback_data=SelectConfirm(confirm=confirm))

    return builder.as_markup()
