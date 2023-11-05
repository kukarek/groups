from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.types import Message
from database import sql 
from ..filters import *
from ..keyboards import *
from misc import server
from ...group_keyboards import group_start_keyboard
from ...group_filters import *
    

async def remove_group(message: Message):
    
    sql.set_tg_user_status(message.from_id, "removing group")

    await message.answer("Вы точно хотите удалить группу?", reply_markup=confirm_remove_keyboard())

async def removing_group(message: Message):

    group = server.get_group(sql.get_current_group_id(message.from_id))
    if server.remove_group(group.GROUP_NAME):

        sql.set_tg_user_status(message.from_id, "None")
        await message.answer("Добро пожаловать в helper bot!", reply_markup=admin_panel_keyboard(message.from_id))
    
async def cancel(message: Message):

    sql.set_tg_user_status(message.from_id, "None")

    group = server.get_group(sql.get_current_group_id(message.from_id))

    await message.answer(f"Управление группой {message.text}", reply_markup=group_start_keyboard(group))

def register_removing_handlers(dp: Dispatcher):

    dp.register_message_handler(remove_group, Text(equals="Удалить группу") & isExistCurrentGroup())
    dp.register_message_handler(removing_group, Text(equals="Удалить") & isRemovingGroup())
    dp.register_message_handler(cancel, Text(equals="Отмена") & isRemovingGroup())