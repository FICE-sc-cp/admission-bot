from aiogram.filters.callback_data import CallbackData

from app.types.genders import Genders


class SelectGender(CallbackData, prefix="gender"):
    gender: Genders
