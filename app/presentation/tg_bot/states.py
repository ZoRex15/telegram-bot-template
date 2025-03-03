from aiogram.fsm.state import State, StatesGroup


class Mailing(StatesGroup):
    MAILING_MENU = State()
    CREATE_MAILING = State()
    FIND_MAILING = State()