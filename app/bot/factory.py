from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.bot.handlers import router as main_router
from app.bot.middlewares.sessionmaker import SessionMaker
from app.settings import settings
from redis import asyncio as aioredis
from aiogram.fsm.storage.redis import RedisStorage


def create_dispatcher() -> Dispatcher:
    redis = aioredis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        username=settings.REDIS_USERNAME,
        password=settings.REDIS_PASSWORD.get_secret_value(),
        decode_responses=True
    )

    storage = RedisStorage(redis=redis)
    dispatcher = Dispatcher(storage=storage)

    engine = create_async_engine(
        URL.create(
            "postgresql+asyncpg",
            username=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD.get_secret_value(),
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            database=settings.POSTGRES_DB,
        ),
        pool_recycle=1800
    )
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

    dispatcher.include_router(main_router)

    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())
    dispatcher.update.middleware(SessionMaker(sessionmaker))

    return dispatcher


def create_bot(token: str) -> Bot:
    return Bot(token=token, parse_mode=ParseMode.HTML)
