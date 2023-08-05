from aiogram.filters.callback_data import CallbackData

from app.types.payment_types import PaymentTypes


class SelectPayment(CallbackData, prefix="payment"):
    payment: PaymentTypes
