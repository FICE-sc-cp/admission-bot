from aiogram.types import Message

from app.messages.commands import THREAD_INFO


async def thread_info(message: Message):
    await message.answer(await THREAD_INFO.render_async(chat_id=message.chat.id, thread_id=message.reply_to_message.message_id))