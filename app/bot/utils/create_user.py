from typing import Dict, Any

from aiogram import Bot

from app.bot.admission_api.types.register_user import RegisterUser
from app.bot.admission_api.users import UserAPI
from app.messages.api import REGISTER_USER
from app.models import User
from app.repositories.uow import UnitOfWork
from app.settings import settings


async def create_user(data: Dict[str, Any], uow: UnitOfWork, bot: Bot):
    async with UserAPI() as user_api:
        response = await user_api.register_user(RegisterUser.model_validate(data))

    data["id"] = response["user"]["id"]
    user = User(**data)
    await uow.users.create(user)

    await bot.send_message(
        settings.ADMIN_CHAT_ID,
        await REGISTER_USER.render_async(user=user),
        settings.QUEUE_THREAD_ID
    )
