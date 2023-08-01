from aiogram.fsm.state import StatesGroup, State


class StartForm(StatesGroup):
    first_name = State()
    last_name = State()
    middle_name = State()
    phone_number = State()
    email = State()
    speciality = State()
    dorm = State()
    print_edbo = State()
