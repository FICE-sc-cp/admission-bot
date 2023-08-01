from aiogram import Bot
from fastapi import APIRouter, Depends

from app.api.stubs import BotStub

main_router = APIRouter(tags=["pryomka"])


@main_router.post('/sendMessage')
async def send_message_handler(uid: str, text: str, parse_mode: str = "HTML", bot: Bot = Depends(BotStub)):
    await bot.send_message(chat_id=uid, text=text, parse_mode=parse_mode)
    return {}


# @main_router.post("/broadcastMessage")
# async def broadcast_handler(request: web.Request):
#     query = await request.json()
#
#     for uid in query['uids']:
#         await bot.send_message(chat_id=uid, text=query['text'],
#                                     parse_mode=query['parse_mode'] if 'parse_mode' in query else None)
#         await asyncio.sleep(1 / 5)  # 5 msg/second
#
#     return {}
