from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database import sql
from ...group_keyboards import *
from misc import server


def group_parameters_keyboard(user_id):

    group = server.get_group(sql.get_current_group_id(user_id))
    admins = sql.get_vk_admins(group.GROUP_ID)

    keyboard = ReplyKeyboardMarkup()

    keyboard.add(KeyboardButton("Добавить админа"))
    if admins:
        keyboard.add(KeyboardButton("Удалить админа"))
    keyboard.add(KeyboardButton("Изменить правила размещения"))
    keyboard.add(KeyboardButton("Изменить пример слов"))
    keyboard.add(KeyboardButton("Изменить слова для поиска топа"))
    keyboard.add(KeyboardButton("Изменить способы оплаты"))
    
    keyboard.add(KeyboardButton("Меню группы"))

    return keyboard

def admins_for_remove_keyboard(admins):
    
    keyboard = ReplyKeyboardMarkup()

    for admin in admins:
        keyboard.add(KeyboardButton(admin))

    keyboard.add(KeyboardButton("Отмена"))

    return keyboard
    