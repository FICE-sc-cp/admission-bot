from aiogram import Router
from aiogram.filters import Command

from app.bot.filters.is_registered import IsRegistered
from app.bot.handlers.help_command import help_command
from app.bot.handlers.start_form import start_without_registration

router = Router()

router.message.register(help_command, Command(commands=["info", "help", "support"]))
router.message.register(start_without_registration, Command("start"), ~IsRegistered())
