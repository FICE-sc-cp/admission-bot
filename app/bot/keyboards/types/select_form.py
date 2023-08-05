from aiogram.filters.callback_data import CallbackData

from app.types.study_forms import StudyForms


class SelectForm(CallbackData, prefix="form"):
    form: StudyForms
