from aiogram.types import Message


async def debug(message: Message):
    await message.answer(f"Chat id: {message.chat.id}\nThread id: {message.reply_to_message.message_id}")