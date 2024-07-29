from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs

from app.bot.middlewares.throttling import ThrottlingMiddleware
from app.bot.handlers import router as main_router


def create_dispatcher() -> Dispatcher:
    storage = MemoryStorage()
    dispatcher = Dispatcher(storage=storage)
    setup_dialogs(dispatcher)

    dispatcher.include_router(main_router)

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
