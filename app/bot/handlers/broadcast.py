from asyncio import sleep

from aiogram import Bot
from aiogram.types import Message
from sqlalchemy import select, func

from app.messages.commands import BROADCAST, BROADCAST_CONTRACT
from app.models import User
from app.repositories.uow import UnitOfWork


async def broadcast(message: Message, uow: UnitOfWork, bot: Bot):
    users = await uow.users.get()
    for user in users:
        try:
            await bot.send_message(user.telegram_id, BROADCAST)
        except:
            await message.answer(f"{user.last_name} {user.first_name} {user.surname}")
        await sleep(0.1)


async def broadcast_contract(message: Message, uow: UnitOfWork, bot: Bot):
    with open("users.txt", "r", encoding='utf-8-sig') as f:
        full_names = list(map(lambda x: x.strip(), f.readlines()))
    session = uow.get_session()
    for full_name in full_names:
        users = (await session.scalars(
            select(User)
            .where(func.trim(User.last_name + " " + User.first_name + " " + func.coalesce(User.surname, "")) == full_name)
        )).all()
        if len(users) >= 1:
            user = users[0]
            try:
                await bot.send_message(user.telegram_id, BROADCAST_CONTRACT)
            except:
                await message.answer(f"{user.last_name} {user.first_name} {user.surname}")
        else:
            await message.answer(f"Не знайдено! {full_name}")
        await sleep(0.2)
