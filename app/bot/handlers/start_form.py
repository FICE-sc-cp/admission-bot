from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.messages.commands import START


async def start_without_registration(message: Message, state: FSMContext):
    await message.answer(START)
