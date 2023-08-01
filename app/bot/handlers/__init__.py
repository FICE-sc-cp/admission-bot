from aiogram import Router
from aiogram.filters import Command

from app.bot.filters.is_registered import IsRegistered
from app.bot.handlers.help_command import help_command
from app.bot.handlers.start_form import start_without_registration, input_first_name, input_last_name, input_surname
from app.bot.states.start_form import StartForm

router = Router()

router.message.register(help_command, Command(commands=["info", "help", "support"]))
router.message.register(start_without_registration, Command("start"), ~IsRegistered())
router.message.register(input_first_name, StartForm.first_name)
router.message.register(input_last_name, StartForm.last_name)
router.message.register(input_surname, StartForm.surname)

