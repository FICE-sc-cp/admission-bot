from aiogram.filters import Filter
from aiogram.types import Message

from app.repositories.uow import UnitOfWork


class IsRegistered(Filter):
    async def __call__(self, message: Message, uow: UnitOfWork):
        user = await uow.users.get_by_id(message.from_user.id)
        if user is not None:
            return {"user": user}
        return False
