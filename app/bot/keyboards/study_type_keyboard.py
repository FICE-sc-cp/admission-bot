from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.select_type import SelectType
from app.types.study_types import StudyTypes


def get_study_type_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for study_type in StudyTypes:
        builder.button(text=study_type, callback_data=SelectType(type=study_type))

    return builder.as_markup()
