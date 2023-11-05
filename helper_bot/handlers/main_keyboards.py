from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from misc.server import groups
from misc.config import OWNER_ID

def admin_panel_keyboard(user_id):

    keyboard = ReplyKeyboardMarkup(row_width=1)

    for group in groups:
        if group.OWNER_ID == user_id:
            keyboard.add(KeyboardButton(group.GROUP_NAME))

    keyboard.add(KeyboardButton("Добавить группу"))

    if user_id == OWNER_ID:
        keyboard.add(KeyboardButton("Добавить пользователя"))

    return keyboard

