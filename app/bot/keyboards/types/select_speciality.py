from aiogram.filters.callback_data import CallbackData

from app.types.specialities import Specialities


class SelectSpeciality(CallbackData, prefix="speciality"):
    speciality: Specialities
