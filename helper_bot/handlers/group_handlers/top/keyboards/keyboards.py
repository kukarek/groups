from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def top_group_keyboard():

    keyboard = ReplyKeyboardMarkup()

    keyboard.add(KeyboardButton("Узнать топ"))
    keyboard.add(KeyboardButton("Удалить ключевые слова"))
    keyboard.add(KeyboardButton("Меню группы"))

    return keyboard
