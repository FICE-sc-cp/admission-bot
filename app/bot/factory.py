from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from app.bot.middlewares.throttling import ThrottlingMiddleware


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()

    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())
    dispatcher.update.middleware(ThrottlingMiddleware())

    return dispatcher


def create_bot(token: str) -> Bot:
    return Bot(
        token=token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
