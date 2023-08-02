from aiogram.filters.callback_data import CallbackData

from app.types.confirms import Confirms


class SelectConfirm(CallbackData, prefix="confirm"):
    confirm: Confirms
