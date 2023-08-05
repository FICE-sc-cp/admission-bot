import email_validator
import phonenumbers
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Bot

from app.bot.keyboards.confirm_keyboard import get_confirm_keyboard
from app.bot.keyboards.menu_keyboard import get_menu_keyboard
from app.bot.keyboards.payment_type_keyboard import get_payment_type_keyboard
from app.bot.keyboards.speciality_keyboard import get_speciality_keyboard
from app.bot.keyboards.study_form_keyboard import get_study_form_keyboard
from app.bot.keyboards.study_type_keyboard import get_study_type_keyboard
from app.bot.keyboards.types.select_confirm import SelectConfirm
from app.bot.keyboards.types.select_form import SelectForm
from app.bot.keyboards.types.select_payment import SelectPayment
from app.bot.keyboards.types.select_speciality import SelectSpeciality
from app.bot.keyboards.types.select_type import SelectType
from app.bot.states.start_form import StartForm
from app.bot.utils.create_user import create_user
from app.bot.utils.replace_apostrophe import replace_apostrophe
from app.messages.commands import START, FIRST_NAME, LAST_NAME, SURNAME, PHONE, EMAIL, DORM, PRINTED_EDBO, MENU, \
    SPECIALITY, CONFIRM_EDBO, STUDY_TYPE, STUDY_FORM, PAYMENT_TYPE
from app.messages.errors import INCORRECT_DATA
from app.repositories.uow import UnitOfWork
from app.settings import settings
from app.types.confirms import Confirms
from app.types.study_types import StudyTypes


async def start_without_registration(message: Message, state: FSMContext):
    await message.answer(START)
    await state.clear()
    await message.answer(FIRST_NAME)
    await state.set_state(StartForm.first_name)


async def input_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=replace_apostrophe(message.text))
    await message.answer(LAST_NAME)
    await state.set_state(StartForm.last_name)


async def input_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=replace_apostrophe(message.text))
    await message.answer(SURNAME)
    await state.set_state(StartForm.middle_name)


async def input_middle_name(message: Message, state: FSMContext):
    await state.update_data(surname=replace_apostrophe(message.text) if message.text != "-" else None)
    await message.answer(PHONE)
    await state.set_state(StartForm.phone_number)


async def input_phone(message: Message, state: FSMContext):
    try:
        phone_number = phonenumbers.parse(message.text)
        if phonenumbers.is_valid_number(phone_number):
            await state.update_data(phone=message.text)
            await message.answer(EMAIL)
            await state.set_state(StartForm.email)
        else:
            await message.answer(INCORRECT_DATA)
    except phonenumbers.phonenumberutil.NumberParseException:
        await message.answer(INCORRECT_DATA)


async def input_email(message: Message, state: FSMContext):
    try:
        email = email_validator.validate_email(message.text)
        await state.update_data(email=email.normalized)
        await message.answer(SPECIALITY, reply_markup=get_speciality_keyboard())
        await state.set_state(StartForm.speciality)
    except email_validator.EmailNotValidError:
        await message.answer(INCORRECT_DATA)


async def input_speciality(callback: CallbackQuery, callback_data: SelectSpeciality, state: FSMContext):
    await state.update_data(speciality=callback_data.speciality)
    await callback.message.edit_reply_markup()
    await callback.message.answer(STUDY_TYPE, reply_markup=get_study_type_keyboard())
    await state.set_state(StartForm.study_type)


async def input_study_type(callback: CallbackQuery, callback_data: SelectType, state: FSMContext):
    await state.update_data(study_type=callback_data.type)
    await callback.message.edit_reply_markup()
    if callback_data.type == StudyTypes.BUDGET:
        await callback.message.answer(STUDY_FORM, reply_markup=get_study_form_keyboard())
        await state.set_state(StartForm.study_form)
    else:
        await callback.message.answer(PAYMENT_TYPE, reply_markup=get_payment_type_keyboard())
        await state.set_state(StartForm.payment_type)


async def input_payment_type(callback: CallbackQuery, callback_data: SelectPayment, state: FSMContext):
    await state.update_data(payment_type=callback_data.payment)
    await callback.message.edit_reply_markup()
    await callback.message.answer(STUDY_FORM, reply_markup=get_study_form_keyboard())
    await state.set_state(StartForm.study_form)


async def input_study_form(callback: CallbackQuery, callback_data: SelectForm, state: FSMContext):
    await state.update_data(study_form=callback_data.form)
    await callback.message.edit_reply_markup()
    await callback.message.answer(DORM, reply_markup=get_confirm_keyboard())
    await state.set_state(StartForm.dorm)


async def input_dorm(callback: CallbackQuery, callback_data: SelectConfirm, state: FSMContext):
    await state.update_data(is_dorm=True if callback_data.confirm == Confirms.YES else False)
    await callback.message.edit_reply_markup()
    await callback.message.answer(CONFIRM_EDBO, reply_markup=get_confirm_keyboard())
    await state.set_state(StartForm.confirm_edbo)


async def input_confirm_edbo(callback: CallbackQuery, callback_data: SelectConfirm, state: FSMContext, uow: UnitOfWork, bot: Bot):
    await state.update_data(confirm_edbo=True if callback_data.confirm == Confirms.YES else False)
    await callback.message.edit_reply_markup()
    if settings.CHECK_EDBO:
        await callback.message.answer(PRINTED_EDBO, reply_markup=get_confirm_keyboard())
        await state.set_state(StartForm.print_edbo)
    else:
        data = await state.get_data()
        data["telegram_id"] = callback.from_user.id
        data["username"] = callback.from_user.username
        await create_user(data, uow, bot)
        await callback.message.answer(MENU, reply_markup=get_menu_keyboard())
        await state.clear()


async def input_edbo(callback: CallbackQuery, callback_data: SelectConfirm, state: FSMContext, uow: UnitOfWork, bot: Bot):
    await state.update_data(printed_edbo=True if callback_data.confirm == Confirms.YES else False)
    data = await state.get_data()
    data["telegram_id"] = callback.from_user.id
    data["username"] = callback.from_user.username
    await create_user(data, uow, bot)

    await callback.message.edit_reply_markup()
    await callback.message.answer(MENU, reply_markup=get_menu_keyboard())
    await state.clear()
