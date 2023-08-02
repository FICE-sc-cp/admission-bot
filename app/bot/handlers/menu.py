from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.bot.keyboards.menu_keyboard import get_menu_keyboard
from app.messages.commands import MENU


async def menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(MENU, reply_markup=get_menu_keyboard())


async def menu_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(MENU, reply_markup=get_menu_keyboard())
