from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    ID = State()


class SendMessage(StatesGroup):
    msg = State()


class VIPPurchaseState(StatesGroup):
    waiting_for_receipt = State()
