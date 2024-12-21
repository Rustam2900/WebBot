from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    ID = State()


class SendMessage(StatesGroup):
    msg = State()
