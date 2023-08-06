from aiogram.types import Message

from app.models import User
from app.repositories.uow import UnitOfWork


async def reset_user(message: Message, uow: UnitOfWork, user: User):
    await uow.users.delete(user.id)
    await message.answer("Користувача видалено")
