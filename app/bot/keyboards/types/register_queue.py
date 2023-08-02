from aiogram.filters.callback_data import CallbackData


class RegisterQueue(CallbackData, prefix="register"):
    id: int
