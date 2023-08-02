from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Усі черги", callback_data='AllQueues'),
                InlineKeyboardButton(text="Мої черги", callback_data='MyQueues'),
            ],
            [
                InlineKeyboardButton(text="ℹ️ Інформація",
                                     url="https://telegra.ph/%D0%86nformac%D1%96ya-pro-elektronnu-chergu-pri-vstup%D1%96-na-F%D0%86OT-cherez-Telegram-bot-fiot-queue-bot-08-26"),
                InlineKeyboardButton(text="🆘 Допомога", url="https://t.me/fiot_help_bot"),
            ],
            # [
            #     InlineKeyboardButton(text="Змінити реєстраційні дані", callback_data='ChangeData'),
            # ]
        ]
    )
