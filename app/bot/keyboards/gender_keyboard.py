from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.select_gender import SelectGender
from app.types.genders import Genders


def get_gender_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for gender in Genders:
        builder.button(text=gender, callback_data=SelectGender(gender=gender))

    return builder.as_markup()
