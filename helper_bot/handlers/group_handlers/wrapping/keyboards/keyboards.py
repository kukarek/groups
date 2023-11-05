from aiogram.types import KeyboardButton, ReplyKeyboardMarkup



def wrapping_panel_keyboard(group):

    keyboard = ReplyKeyboardMarkup()

    if group.isActiveWrapping:
        keyboard.add(KeyboardButton("Остановить накрутку"))
    else: 
        keyboard.add(KeyboardButton("Запустить накрутку"))

    if group.OWNER_ID == 1020541698:
        keyboard.add(KeyboardButton("Баланс"))

    keyboard.add(KeyboardButton("Меню группы"))

    return keyboard


