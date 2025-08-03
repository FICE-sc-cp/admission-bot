from aiogram import Router
from aiogram.filters import Command, CommandStart

from app.bot.handlers.debug import debug
from app.bot.handlers.register import form
from app.bot.handlers.start import start

router = Router()

router.message.register(debug, Command("debug"))
router.message.register(start, CommandStart())
router.include_router(form)