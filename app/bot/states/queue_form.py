from aiogram.fsm.state import StatesGroup, State


class QueueForm(StatesGroup):
    geo = State()
