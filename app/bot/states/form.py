from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    email = State()

    hostel = State()
    edbo = State()
    speciality = State()

    contact = State()
    geo = State()
