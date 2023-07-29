from aiogram import types


def divide_chunks(a, n):
    for i in range(0, len(a), n):
        yield a[i:i + n]


def get_geo_kbd(lang='ua'):
    return types.ReplyKeyboardMarkup(
        # aiogram requests lists instead of iterables as keyboard initializer, idk why
        one_time_keyboard=True,
        keyboard=[
            [
                types.KeyboardButton("🌍 Надіслати розташування", request_location=True)
            ]
        ],
        resize_keyboard=True
    )


# def get_reg_kbd(lang='ua'):
#     return types.InlineKeyboardMarkup(
#         row_width=1,
#         inline_keyboard=(
#             (
#                 types.InlineKeyboardButton(t('CERT_REG_BTN', locale=lang), callback_data='CertReg'),
#             ),
#             (
#                 types.InlineKeyboardButton(t('MANUAL_REG_BTN', locale=lang), callback_data='ManualReg'),
#             )
#         )
#     )


def get_menu_kbd(lang='ua', opt_reg_done: bool = False):
    if opt_reg_done:
        return types.InlineKeyboardMarkup(
            row_width=2,
            inline_keyboard=(
                (
                    types.InlineKeyboardButton("Усі черги", callback_data='AllQueues'),
                    types.InlineKeyboardButton("Мої черги", callback_data='MyQueues'),
                ),
                (
                    types.InlineKeyboardButton("ℹ️ Інформація", url="https://telegra.ph/%D0%86nformac%D1%96ya-pro-elektronnu-chergu-pri-vstup%D1%96-na-F%D0%86OT-cherez-Telegram-bot-fiot-queue-bot-08-26"),
                    types.InlineKeyboardButton("🆘 Допомога", url="https://t.me/fiot_help_bot"),
                ),
                (
                    types.InlineKeyboardButton("Змінити реєстраційні дані", callback_data='ChangeData'),
                )
            )
        )
    else:
        return types.InlineKeyboardMarkup(
            row_width=2,
            inline_keyboard=(
                (
                    types.InlineKeyboardButton("❗️ Продовжити реєстрацію ❗️", callback_data='OptReg'),
                ),
                (
                    types.InlineKeyboardButton("Усі черги", callback_data='AllQueues'),
                    types.InlineKeyboardButton("Мої черги", callback_data='MyQueues'),
                ),
                (
                    types.InlineKeyboardButton("ℹ️ Інформація", url="https://telegra.ph/%D0%86nformac%D1%96ya-pro-elektronnu-chergu-pri-vstup%D1%96-na-F%D0%86OT-cherez-Telegram-bot-fiot-queue-bot-08-26"),
                    types.InlineKeyboardButton("🆘 Допомога", url="https://t.me/fiot_help_bot"),
                ),
                (
                    types.InlineKeyboardButton("Змінити реєстраційні дані", callback_data='ChangeData'),
                )
            )
        )


def get_info_kbd(lang='ua'):
    return types.InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=(
            (
                types.InlineKeyboardButton("ℹ️ Інформація", url="https://telegra.ph/%D0%86nformac%D1%96ya-pro-elektronnu-chergu-pri-vstup%D1%96-na-F%D0%86OT-cherez-Telegram-bot-fiot-queue-bot-08-26"),
            ),
            (
                types.InlineKeyboardButton("🆘 Допомога", url="https://t.me/fiot_help_bot"),
            ),
        )
    )


def get_to_menu_kbd(lang='ua'):
    return types.InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=(
            (
                types.InlineKeyboardButton("🔙 Повернутися у меню", callback_data='Menu'),
            ),
        )
    )


def get_queues_kbd(queues, my_queues=False, lang='ua'):
    queues = filter(lambda x: x['active'], queues)
    kbd = list(types.InlineKeyboardButton(queue['name'], callback_data=f'GetMyQueue{queue["id"]}'
                                                                       if my_queues else f'GetQueue{queue["id"]}')
               for queue in queues)
    return types.InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=list(divide_chunks(kbd, 2)) + [[types.InlineKeyboardButton("🔙 Повернутися у меню",
                                                                                   callback_data='Menu')]]
    )


def get_update_my_queue_kbd(queue_id, lang='ua'):
    return types.InlineKeyboardMarkup(
        inline_keyboard=(
            (
                types.InlineKeyboardButton("🔄 Оновити", callback_data=f'GetMyQueue{queue_id}'),
            ),
            (
                types.InlineKeyboardButton("🏃 Покинути чергу", callback_data=f'LeaveQueue{queue_id}'),
            ),
            (
                types.InlineKeyboardButton("🔙 Повернутися у меню", callback_data='Menu'),
            )
        )
    )


def get_register_in_queue_kbd(queue_id, lang='ua'):
    return types.InlineKeyboardMarkup(
        inline_keyboard=(
            (
                types.InlineKeyboardButton("Зареєструватися у черзі", callback_data=f'RegInQueue{queue_id}'),
            ),
            (
                types.InlineKeyboardButton("🔙 Повернутися у меню", callback_data='Menu'),
            )
        )
    )
