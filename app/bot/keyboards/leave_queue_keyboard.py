from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.leave_queue import LeaveQueue


def get_leave_queue_keyboard(queue_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Так", callback_data=LeaveQueue(id=queue_id, confirm=True))
    builder.button(text="🔙 Повернутися у меню", callback_data="Menu")
    builder.adjust(1)

    return builder.as_markup()
