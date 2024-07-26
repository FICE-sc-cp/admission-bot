import logging

from mangum import Mangum

from app.api.factory import create_app
from app.bot.factory import create_bot, create_dispatcher
from app.settings import settings

logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

bot = create_bot(token=settings.BOT_TOKEN.get_secret_value())
dispatcher = create_dispatcher()
app = create_app(
    bot=bot,
    dispatcher=dispatcher,
    webhook_secret=settings.TELEGRAM_SECRET.get_secret_value()
)
handler = Mangum(app)
