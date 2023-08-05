from aiogram.filters.callback_data import CallbackData

from app.types.study_types import StudyTypes


class SelectType(CallbackData, prefix="type"):
    type: StudyTypes
