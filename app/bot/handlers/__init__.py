from aiogram import Router
from aiogram.filters import Command

from app.bot.handlers.help_command import help_command

router = Router()

router.message.register(help_command, Command(commands=["info", "help", "support"]))
