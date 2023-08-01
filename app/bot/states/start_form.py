from aiogram.fsm.state import StatesGroup, State


class StartForm(StatesGroup):
    first_name = State()
    last_name = State()
    surname = State()
