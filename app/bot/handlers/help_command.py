from aiogram.types import Message

from app.bot.keyboards.info_keyboard import get_info_keyboard
from app.messages.commands import HELP


async def help_command(message: Message):
    await message.reply(HELP, reply_markup=get_info_keyboard())
