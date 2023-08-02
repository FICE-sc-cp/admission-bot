from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.register_queue import RegisterQueue


def get_register_queue_keyboard(queue_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Зареєструватися у черзі", callback_data=RegisterQueue(id=queue_id))
    builder.button(text="🔙 Повернутися у меню", callback_data="menu")
    builder.adjust(1)

    return builder.as_markup()