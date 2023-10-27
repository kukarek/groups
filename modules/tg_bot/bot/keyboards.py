from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from ..functions.wrapping.states import wrapping



def admin_panel_keyboard():

    keyboard = ReplyKeyboardMarkup(row_width=1)

    keyboard.add(KeyboardButton("Получить топ"))
    keyboard.add(KeyboardButton("Баланс"))
    keyboard.add(KeyboardButton("Накрутка"))

    return keyboard


def wrapping_panel_keyboard():

    keyboard = ReplyKeyboardMarkup(row_width=1)

    if wrapping.isActive:
        keyboard.add(KeyboardButton("Остановить накрутку"))
        keyboard.add(KeyboardButton("Состояние накрутки"))
    else: 
        keyboard.add(KeyboardButton("Запустить накрутку"))

    keyboard.add(KeyboardButton("Главное меню"))

    return keyboard

def wrapping_state_panel_keyboard():

    keyboard = ReplyKeyboardMarkup(row_width=1)

    if wrapping.TG:
        keyboard.add(KeyboardButton("Отключить телеграм"))
    else:
        keyboard.add(KeyboardButton("Включить телеграм"))

    if wrapping.VK:
        keyboard.add(KeyboardButton("Отключить вк"))
    else:
        keyboard.add(KeyboardButton("Включить вк"))
    
    keyboard.add(KeyboardButton("Главное меню"))

    return keyboard

def wrapping_start_panel_keyboard():

    keyboard = ReplyKeyboardMarkup(row_width=1)

    keyboard.add(KeyboardButton("Цикл"))
    keyboard.add(KeyboardButton("Таймер"))

    if wrapping.TG:
        keyboard.add(KeyboardButton("Отключить телеграм"))
    else:
        keyboard.add(KeyboardButton("Включить телеграм"))

    if wrapping.VK:
        keyboard.add(KeyboardButton("Отключить вк"))
    else:
        keyboard.add(KeyboardButton("Включить вк"))
    
    keyboard.add(KeyboardButton("Запустить"))
    
    keyboard.add(KeyboardButton("Главное меню"))

    return keyboard

