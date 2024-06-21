from aiogram.dispatcher.filters.state import State, StatesGroup


class MyStates(StatesGroup):
    ism = State()
    familya = State()
    ph_number = State()


class Kirim(StatesGroup):
    kirim = State()
    sabab = State()


class Chiqim(StatesGroup):
    chiqim = State()
    sabab = State()
