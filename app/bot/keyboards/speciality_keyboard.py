from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.select_speciality import SelectSpeciality
from app.types.specialities import Specialities


def get_speciality_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for speciality in Specialities:
        builder.button(text=speciality, callback_data=SelectSpeciality(speciality=speciality))

    return builder.as_markup()
