from aiogram import Bot
from aiogram.types import Message

from app.messages.commands import BROADCAST
from app.repositories.uow import UnitOfWork


async def broadcast(message: Message, uow: UnitOfWork, bot: Bot):
    users = await uow.users.get()
    for user in users:
        try:
            await bot.send_message(user.telegram_id, BROADCAST)
        except:
            await message.answer(f"{user.last_name} {user.first_name} {user.surname}")