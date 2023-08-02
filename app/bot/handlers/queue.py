from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, FSInputFile
from aiogram.fsm.context import FSMContext

from app.bot.admission_api.queue import QueueAPI
from app.bot.admission_api.users import UserAPI
from app.bot.keyboards.geo_keyboard import get_geo_keyboard
from app.bot.keyboards.leave_queue_keyboard import get_leave_queue_keyboard
from app.bot.keyboards.menu_keyboard import get_menu_keyboard
from app.bot.keyboards.queues_keyboard import get_queues_keyboard
from app.bot.keyboards.register_queue_keyboard import get_register_queue_keyboard
from app.bot.keyboards.types.leave_queue import LeaveQueue
from app.bot.keyboards.types.register_queue import RegisterQueue
from app.bot.keyboards.types.select_queue import SelectQueue
from app.bot.keyboards.update_queue_keyboard import get_update_queue_keyboard
from app.messages.commands import SELECT_QUEUE, MY_QUEUES, SEND_GEOLOCATION, YOU_NOT_IN_QUEUE, LEAVE_QUEUE, MENU
from app.messages.errors import NO_QUEUES, NO_REGISTERED
from app.bot.states.queue_form import QueueForm
from app.bot.utils.get_spherical_distance import get_spherical_distance
from app.models import User
from app.settings import settings


async def all_queues(callback: CallbackQuery):
    async with QueueAPI() as queue_api:
        queues = (await queue_api.list_queues())['queues']
    num = len(list(filter(lambda x: x['active'], queues)))
    if num > 0:
        await callback.message.edit_text(SELECT_QUEUE,
                                         reply_markup=get_queues_keyboard(queues, my_queues=False))
    else:
        await callback.answer(NO_QUEUES)


async def my_queues(callback: CallbackQuery, user: User):
    async with UserAPI() as user_api:
        user_data = await user_api.get_user_info(user.id)
    queues = user_data['queues']
    num = len(list(filter(lambda x: x['active'], queues)))
    if num > 0:
        await callback.message.edit_text(MY_QUEUES,
                                         reply_markup=get_queues_keyboard(queues, my_queues=True))
    else:
        await callback.answer(NO_REGISTERED)


async def get_my_queue(callback: CallbackQuery, callback_data: SelectQueue, user: User):
    async with UserAPI() as user_api:
        user_data = await user_api.get_user_info(user.id)
        queues = user_data['queues']
    queue_id = callback_data.id
    queue = list(filter(lambda x: queue_id == x['id'], queues))
    if not queue:
        await callback.answer(YOU_NOT_IN_QUEUE)
        return

    if queue['position']['status'] == 'processing':
        await callback.message.edit_text(
            "<b>{queue_name}</b>\nВаша заявка оброблюється оператором, можете заходити до корпусу.".format(
                queue_name=queue['name']),
            reply_markup=get_update_queue_keyboard(queue_id))

    elif queue['position']['status'] == 'waiting':
        await callback.message.edit_text(
            "<b>{queue_name}</b>\nВаша позиція у черзі: {pos}\nВаш ідентифікаційний номер у черзі: {abs_pos}".format(
                queue_name=queue['name'],
                pos=queue['position']['relativePosition'],
                abs_pos=queue['position']['code']),
            reply_markup=get_update_queue_keyboard(queue_id))


async def get_queue(callback: CallbackQuery, state: FSMContext, callback_data: SelectQueue, user: User):
    async with UserAPI() as user_api:
        user_data = await user_api.get_user_info(user.id)
        queues = user_data['queues']
    queue_id = callback_data.id
    if any(map(lambda x: queue_id == x['id'], queues)):
        await get_my_queue(callback, callback_data, user)
        return
    else:
        await state.set_state(QueueForm.geo)
        await state.update_data(queue_id=queue_id)
        return await callback.message.answer(
            SEND_GEOLOCATION,
            reply_markup=get_geo_keyboard())


async def leave_queue(callback: CallbackQuery, callback_data: LeaveQueue):
    await callback.message.edit_text(LEAVE_QUEUE, reply_markup=get_leave_queue_keyboard(callback_data.id))


async def confirm_leave_queue(callback: CallbackQuery, callback_data: LeaveQueue, user: User):
    async with QueueAPI() as queue_api:
        await queue_api.remove_user_from_queue(callback_data.id, user.id)
    await callback.message.edit_text(MENU, reply_markup=get_menu_keyboard())


async def location_handler(message: Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude

    data = await state.get_data()
    queue_id = data.get("queue_id", -1)

    if (get_spherical_distance(lat, lon) > settings.RADIUS) or \
            (message.forward_from is not None):
        return await message.reply(
            "Помилка! Ви ще не знаходитесь на території КПІ, надішліть геолокацію ще раз, коли будете на місці, чи натисніть \"/start\" щоб повернутись у меню\".",
            reply_markup=get_geo_keyboard())
    else:
        await state.clear()
        await message.reply("Ви знаходитесь на КПІ!",
                            reply_markup=ReplyKeyboardRemove())

        await message.reply("Ви дійсно хочете зареєструватись у цій черзі?",
                            reply_markup=get_register_queue_keyboard(queue_id))


async def register_queue(callback: CallbackQuery, callback_data: RegisterQueue, user: User):
    queue_id = callback_data.id
    async with QueueAPI() as queue_api:
        data = await queue_api.add_user_to_queue(queue_id, user.id)
    if "message" in data:
        await callback.answer(data['message'])
        return

    await callback.message.answer_photo(FSInputFile(f'q_nums/{data["position"]["code"]}.jpg'),
                                        caption="Ваш ідентифікаційний номер у черзі")
    new_callback_data = SelectQueue(id=queue_id, is_my=True)
    await get_my_queue(callback, new_callback_data, user)
