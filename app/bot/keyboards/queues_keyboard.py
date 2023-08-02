from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.select_queue import SelectQueue


def get_queues_keyboard(queues, my_queues=False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    queues = filter(lambda x: x['active'], queues)
    for queue in queues:
        builder.button(text=queue["name"], callback_data=SelectQueue(id=queue["id"], is_my=my_queues))

    builder.button(text="🔙 Повернутися у меню", callback_data="menu")
    builder.adjust(1)

    return builder.as_markup()
