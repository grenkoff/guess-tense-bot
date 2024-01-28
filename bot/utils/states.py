from aiogram.fsm.state import StatesGroup, State


class GuessRandom(StatesGroup):
    guess_random = State()
    finish_next = State()
