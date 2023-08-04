import logging

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.api.factory import create_app
from app.bot.factory import create_bot, create_dispatcher
from app.settings import settings

logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

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

bot = create_bot(token=settings.BOT_TOKEN.get_secret_value())
dispatcher = create_dispatcher(sessionmaker)
app = create_app(
    bot=bot,
    dispatcher=dispatcher,
    webhook_secret=settings.TELEGRAM_SECRET.get_secret_value(),
    sessionmaker=sessionmaker
)
