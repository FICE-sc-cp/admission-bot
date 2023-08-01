from typing import Dict, Any

from app.bot.admission_api.types.register_user import RegisterUser
from app.bot.admission_api.users import UserAPI
from app.models import User
from app.repositories.uow import UnitOfWork


async def create_user(data: Dict[str, Any], uow: UnitOfWork):
    user = User(**data)
    await uow.users.create(user)

    async with UserAPI() as user_api:
        await user_api.register_user(RegisterUser.model_validate(user, from_attributes=True))