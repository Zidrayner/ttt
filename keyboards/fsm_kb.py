from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_fsm_kb(lst: list) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in lst]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)