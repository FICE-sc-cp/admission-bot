from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.keyboards.gender_keyboard import get_gender_keyboard
from app.bot.messages.commands import START, FIRST_NAME, LAST_NAME, SURNAME, GENDER
from app.bot.states.start_form import StartForm


async def start_without_registration(message: Message, state: FSMContext):
    await message.answer(START)
    await state.clear()
    await message.answer(FIRST_NAME)
    await state.set_state(StartForm.first_name)


async def input_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer(LAST_NAME)
    await state.set_state(StartForm.last_name)


async def input_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer(SURNAME)
    await state.set_state(StartForm.surname)


async def input_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text if message.text != "-" else None)
    await message.answer(GENDER, reply_markup=get_gender_keyboard())
    await state.set_state(StartForm.last_name)


