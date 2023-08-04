from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Усі черги", callback_data='AllQueues'),
                InlineKeyboardButton(text="Мої черги", callback_data='MyQueues'),
            ],
            [
                InlineKeyboardButton(text="🆘 Допомога", url="https://t.me/fiot_help_bot"),
            ],
            # [
            #     InlineKeyboardButton(text="Змінити реєстраційні дані", callback_data='ChangeData'),
            # ]
        ]
    )
