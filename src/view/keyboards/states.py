from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    city = State()
    org_type = State()
    status_check = State()
    download = State()
