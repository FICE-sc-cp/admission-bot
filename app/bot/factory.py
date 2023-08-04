from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.bot.handlers import router as main_router
from app.bot.middlewares.sessionmaker import SessionMaker
from app.bot.middlewares.throttling import ThrottlingMiddleware
from app.settings import settings


def create_dispatcher(sessionmaker: async_sessionmaker[AsyncSession]) -> Dispatcher:
    redis = aioredis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        username=settings.REDIS_USERNAME,
        password=settings.REDIS_PASSWORD.get_secret_value(),
        decode_responses=True
    )

    storage = RedisStorage(redis=redis)
    dispatcher = Dispatcher(storage=storage)

    dispatcher.include_router(main_router)

    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())
    dispatcher.update.middleware(SessionMaker(sessionmaker))
    dispatcher.update.middleware(ThrottlingMiddleware())

    return dispatcher


def create_bot(token: str) -> Bot:
    return Bot(token=token, parse_mode=ParseMode.HTML)
