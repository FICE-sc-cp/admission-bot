from aiogram.filters.callback_data import CallbackData


class SelectQueue(CallbackData, prefix="queue"):
    id: int
    my_queue: bool
