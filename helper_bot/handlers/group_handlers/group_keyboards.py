from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from ..main_keyboards import *


def group_start_keyboard(group):

    keyboard = ReplyKeyboardMarkup()

    keyboard.add(KeyboardButton("Узнать топ"))
    keyboard.add(KeyboardButton("Накрутка"))
    keyboard.add(KeyboardButton("Отложка"))
    keyboard.add(KeyboardButton("Редактировать"))
    if group.isActiveBot:
        keyboard.add(KeyboardButton("Остановить чат-бота"))
    else:
        keyboard.add(KeyboardButton("Запустить чат-бота"))

    keyboard.add(KeyboardButton("Удалить группу"))
    keyboard.add(KeyboardButton("Главное меню"))

    return keyboard
