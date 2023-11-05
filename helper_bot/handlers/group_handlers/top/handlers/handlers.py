from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
import logging
from database import sql
from misc import server 
from ..filters import *

async def get_top(message: Message):
    
    logging.debug(f"user {message.from_id} join in 'get_top' function")

    group_id = sql.get_current_group_id(message.from_id)

    group = server.get_group(group_id)

    if group.SEARCH_KEYWORDS:

        top = group.Get_top(group_id)

        await message.answer(f"Место в топе по {group.GROUP_NAME}: {top}")
    
    else:

        sql.set_tg_user_status(message.from_id, "adding top keywords")

        await message.answer("Введите ключевые слова через запятую для поиска группы в топе:")

async def adding_top_keywords(message: Message):

    logging.debug(f"user {message.from_id} join in 'adding_top_keywords' function")

    sql.set_tg_user_status(message.from_id, "None")

    group = server.get_group(sql.get_current_group_id(message.from_id))

    group.SEARCH_KEYWORDS = message.text.split(",")

    await message.answer("Ключевые слова для поиска добавлены!")

async def remove_top_keywords(message: Message):

    logging.debug(f"user {message.from_id} join in 'remove_top_keywords' function")

    group = server.get_group(sql.get_current_group_id(message.from_id))

    group.SEARCH_KEYWORDS = []

    await message.answer("Ключевые слова для поиска удалены!")


def register_vktop_handlers(dp: Dispatcher):

    dp.register_message_handler(get_top, Text(equals="Узнать топ") & isUser() & isExistCurrentGroup())
    dp.register_message_handler(adding_top_keywords, isAddingTopKeywords())
    dp.register_message_handler(remove_top_keywords, Text(equals="Удалить ключевые слова") & isUser() & isExistCurrentGroup())