from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from app.bot.states.form import Form


async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(Form.email, mode=StartMode.RESET_STACK)
