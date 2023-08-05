from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.select_payment import SelectPayment
from app.types.payment_types import PaymentTypes


def get_payment_type_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for payment in PaymentTypes:
        builder.button(text=payment, callback_data=SelectPayment(payment=payment))

    return builder.as_markup()
