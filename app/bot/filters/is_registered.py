from aiogram.filters import Filter
from aiogram.types import Message

from app.repositories.uow import UnitOfWork
from app.repositories.user import UserFilter


class IsRegistered(Filter):
    async def __call__(self, message: Message, uow: UnitOfWork):
        user = await uow.users.find_one(UserFilter(telegram_id=message.from_user.id))
        if user is not None:
            return {"user": user}
        return False
