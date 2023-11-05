from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from ....main_keyboards import *



def confirm_remove_keyboard():

    keyboard = ReplyKeyboardMarkup()

    keyboard.add(KeyboardButton("Удалить"))
    keyboard.add(KeyboardButton("Отмена"))

    return keyboard
