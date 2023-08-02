from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.leave_queue import LeaveQueue
from app.bot.keyboards.types.select_queue import SelectQueue


def get_update_queue_keyboard(queue_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="🔄 Оновити", callback_data=SelectQueue(id=queue_id, is_my=True))
    builder.button(text="🏃 Покинути чергу", callback_data=LeaveQueue(id=queue_id))
    builder.button(text="🔙 Повернутися у меню", callback_data="menu")
    builder.adjust(1)

    return builder.as_markup()
