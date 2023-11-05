from aiogram.types import Message
from aiogram.dispatcher.filters import Text
import logging
from aiogram import Dispatcher
from .main_keyboards import *
from database.sql import set_tg_user_status, set_current_group, add_tg_user
from .main_filters import *

from .addind_group import register_adding_group_handlers
from .group_handlers import register_group_handlers



async def on_start(message: Message):

    set_tg_user_status(message.from_id, "None")
    set_current_group(message.from_id, "None")

    logging.debug(f"user {message.from_id} join in 'on_start' function")

    await message.answer("Добро пожаловать в helper bot!", reply_markup=admin_panel_keyboard(message.from_id))

async def send_log(message: Message):

    logging.debug(f"user {message.from_id} join in 'send_log' function")
    with open('log/log.log', 'rb') as log_file:
        await message.answer_document(document=log_file)

async def add_user(message: Message):

    logging.debug(f"user {message.from_id} join in 'add_user' function")
    set_tg_user_status(message.from_id, "adding user")

    await message.answer("Введите id пользователя:")

async def adding_user(message: Message):

    logging.debug(f"user {message.from_id} join in 'adding_user' function")
    set_tg_user_status(message.from_id, "None")

    add_tg_user(message.text)

    await message.answer("Пользователь добавлен!", reply_markup=admin_panel_keyboard(message.from_id))

def register_all_handlers(dp: Dispatcher):

    dp.register_message_handler(on_start, isUser(), commands=['start'])
    dp.register_message_handler(on_start, Text(equals="Главное меню") & isUser())

    dp.register_message_handler(add_user, Text(equals="Добавить пользователя") & isOwner())
    dp.register_message_handler(send_log, isOwner(), commands=("log"))

    register_adding_group_handlers(dp)
    register_group_handlers(dp)
