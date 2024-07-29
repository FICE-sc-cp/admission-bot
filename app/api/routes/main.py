import asyncio

from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from fastapi import APIRouter, Depends

from app.api.schemas.broadcast_message import BroadcastMessage
from app.api.schemas.contract import Contract
from app.api.schemas.user import UserSchema
from app.api.stubs import BotStub
from app.messages.api import CONTRACT_INFO, GOING_USER, REGISTER_USER
from app.settings import settings

main_router = APIRouter(tags=["admission"])


@main_router.post('/sendMessage')
async def send_message_handler(uid: str, text: str, parse_mode: ParseMode = ParseMode.HTML,
                               bot: Bot = Depends(BotStub)):
    await bot.send_message(chat_id=uid, text=text, parse_mode=parse_mode)
    return {}


@main_router.post("/broadcastMessage")
async def broadcast_handler(request: BroadcastMessage, bot: Bot = Depends(BotStub)):
    async def send():
        for uid in request.uids:
            await bot.send_message(chat_id=uid, text=request.text, parse_mode=request.parse_mode)
            await asyncio.sleep(1 / 5)  # 5 msg/second

    asyncio.ensure_future(send())

    return {}


@main_router.post("/sendContract")
async def send_document(contract: Contract, bot: Bot = Depends(BotStub)):
    await bot.send_message(
        settings.ADMIN_CHAT_ID,
        await CONTRACT_INFO.render_async(contract=contract),
        message_thread_id=settings.CONTRACT_THREAD_ID
    )
    return contract


@main_router.post("/sendGoingUser")
async def send_going_user(user: UserSchema, bot: Bot = Depends(BotStub)):
    await bot.send_message(
        settings.ADMIN_CHAT_ID,
        await GOING_USER.render_async(user=user),
        message_thread_id=settings.GOING_THREAD_ID
    )
    return user


@main_router.post("/sendRegistrationInQueue")
async def send_registration_user(user: UserSchema, bot: Bot = Depends(BotStub)):
    await bot.send_message(
        settings.ADMIN_CHAT_ID,
        await REGISTER_USER.render_async(user=user),
        message_thread_id=settings.QUEUE_THREAD_ID
    )
    return user
