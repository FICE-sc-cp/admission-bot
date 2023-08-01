from aiogram.fsm.state import StatesGroup, State


class StartForm(StatesGroup):
    first_name = State()
    last_name = State()
    surname = State()
    phone_number = State()
    email = State()
    dorm = State()
    print_edbo = State()
