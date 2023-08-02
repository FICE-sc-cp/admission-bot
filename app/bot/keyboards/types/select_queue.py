from aiogram.filters.callback_data import CallbackData


class SelectQueue(CallbackData, prefix="queue"):
    id: int
    is_my: bool
