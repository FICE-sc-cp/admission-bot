from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.menu_keyboard import get_menu_keyboard
from app.bot.messages.commands import MENU


async def menu(callback: CallbackQuery):
    await callback.message.edit_text(MENU, reply_markup=get_menu_keyboard())


async def menu_start(message: Message):
    await message.answer(MENU, reply_markup=get_menu_keyboard())
