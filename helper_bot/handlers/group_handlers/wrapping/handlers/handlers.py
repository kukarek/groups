from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.types import Message
import logging
from database import sql  
from ..filters import *
from ..keyboards import *
from misc import server


async def wrapping_panel(message: Message):
    
    logging.debug(f"user {message.from_id} join in 'wrapping_panel' function")
    
    group = server.get_group(sql.get_current_group_id(message.from_id))

    await message.answer("Панель накрутки:", reply_markup=wrapping_panel_keyboard(group))

async def balance(message: Message):
    
    logging.debug(f"user {message.from_id} join in 'balance' function")

    group = server.get_group(sql.get_current_group_id(message.from_id))

    try:
        balance = group.get_balance()
        await message.answer(f"Текущий баланс: {balance}")
    except Exception as e:
        logging.error(e)
    
async def stop_wrapping(message: Message):
    
    logging.debug(f"user {message.from_id} stopped wrapping")

    group = server.get_group(sql.get_current_group_id(message.from_id))
    group.stop_wrapping()
    
    await message.answer("Накрутка остановлена!", reply_markup=wrapping_panel_keyboard(group))

async def start_wrapping(message: Message):

    logging.debug(f"user {message.from_id} started wrapping")

    group = server.get_group(sql.get_current_group_id(message.from_id))
    group.start_wrapping()

    await message.answer("Накрутка запущена!", reply_markup=wrapping_panel_keyboard(group))


def register_wrapping_handlers(dp: Dispatcher):

    dp.register_message_handler(wrapping_panel, Text(equals="Накрутка") & isUser() & isExistCurrentGroup())

    dp.register_message_handler(balance, Text(equals="Баланс") & isOwner() & isExistCurrentGroup())
    
    dp.register_message_handler(stop_wrapping,  Text(equals="Остановить накрутку") & isUser() & isExistCurrentGroup())
    dp.register_message_handler(start_wrapping, Text(equals="Запустить накрутку") & isUser() & isExistCurrentGroup())

