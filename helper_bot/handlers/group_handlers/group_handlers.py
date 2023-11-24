from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from .group_filters import *
from .group_keyboards import *
from aiogram.types import Message
from misc import server 
from database import sql 

from .top.handlers import register_vktop_handlers
from .wrapping import register_wrapping_handlers
from .delay import register_delay_handlers
from .parameters import register_group_param_handlers
from .removing_group import register_removing_handlers

async def group_hand(message: Message):

    for group in server.groups:
        if group.GROUP_NAME == message.text or group.GROUP_ID == int(sql.get_current_group_id(message.from_id)):
            sql.set_current_group(message.from_id, group.GROUP_ID)
            sql.set_tg_user_status(message.from_id, "None")
            await message.answer(f"Управление группой", reply_markup=group_start_keyboard(group))
    
async def start_chat_bot(message: Message):

    group = server.get_group(sql.get_current_group_id(message.from_id))

    group.start()

    await message.answer(f"Чат-бот запущен!", reply_markup=group_start_keyboard(group))

async def stop_bot(message: Message):

    group = server.get_group(sql.get_current_group_id(message.from_id))

    group.stop_chat_bot()

    await message.answer(f"Чат-бот остановлен!", reply_markup=group_start_keyboard(group))



def register_group_handlers(dp: Dispatcher):

    dp.register_message_handler(group_hand, isUser() & isNoCurrentGroup())
    dp.register_message_handler(group_hand, Text(equals="Меню группы") & isUser())

    dp.register_message_handler(start_chat_bot, Text(equals="Запустить чат-бота") & isExistCurrentGroup())
    dp.register_message_handler(stop_bot, Text(equals="Остановить чат-бота") & isExistCurrentGroup())

    register_vktop_handlers(dp)
    register_wrapping_handlers(dp)
    register_delay_handlers(dp)
    register_group_param_handlers(dp)
    register_removing_handlers(dp)