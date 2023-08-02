from aiogram.filters.callback_data import CallbackData


class LeaveQueue(CallbackData, prefix="leave"):
    id: int
    confirm: bool = False
