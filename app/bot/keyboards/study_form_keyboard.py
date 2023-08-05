from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.select_form import SelectForm
from app.types.study_forms import StudyForms


def get_study_form_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for form in StudyForms:
        builder.button(text=form, callback_data=SelectForm(form=form))

    return builder.as_markup()
