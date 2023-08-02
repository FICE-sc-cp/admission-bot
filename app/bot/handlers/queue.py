from aiogram.types import CallbackQuery

from app.bot.admission_api.queue import QueueAPI
from app.bot.admission_api.users import UserAPI
from app.bot.keyboards.queues_keyboard import get_queues_keyboard
from app.bot.messages.commands import SELECT_QUEUE, MY_QUEUES
from app.bot.messages.errors import NO_QUEUES, NO_REGISTERED
from app.models import User


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


