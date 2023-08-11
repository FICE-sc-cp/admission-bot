from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.select_speciality import SelectSpeciality
from app.types.specialities import Specialities


def get_speciality_keyboard(selected: List[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for speciality in Specialities:
        addition = ""
        if speciality in selected:
            addition = "✅"
        builder.button(text=addition + speciality, callback_data=SelectSpeciality(speciality=speciality))
    builder.button(text="Підтвердити", callback_data="confirm_specialty")
    builder.adjust(3)

    return builder.as_markup()
