from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_geo_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(
                text="🌍 Надіслати розташування",
                request_location=True,
            )
        ]],
        one_time_keyboard=True,
        resize_keyboard=True
    )
