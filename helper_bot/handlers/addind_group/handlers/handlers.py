from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from log import loggHandler
from database import sql 
from ....handlers.group_handlers.group_filters import *
from ..filters import *
from misc import server
from ....group import Group
from ...main_keyboards import *

group_id = None
logger = logging.getLogger()

async def add_group(message: Message):
    
    logging.debug(f"user {message.from_id} join in 'add_group' function")

    sql.set_tg_user_status(message.from_id, "adding group id")
    
    await message.answer("Пришлите id вашей группы:")

async def adding_group_id(message: Message):

    logging.debug(f"user {message.from_id} join in 'adding_group_id' function")

    global group_id
    group_id = message.text
    
    group_ids = [str(id) for id in sql.get_group_ids()]
    
    if message.text in group_ids:

        await message.answer("Группа уже добавлена, введите корректный id")

    else:
        sql.add_group(group_id, message.from_id)
        
        sql.set_tg_user_status(message.from_id, "adding group name")

        await message.answer("Пришлите имя вашей группы, пример: rabotakazank")

async def adding_group_name(message: Message):
    
    logging.debug(f"user {message.from_id} join in 'adding_group_name' function")

    sql.set_group_value(group_id, "GROUP_NAME", message.text)

    sql.set_tg_user_status(message.from_id, "adding vk token")

    await message.answer("Введите токен вк с правами управления сообщениями:")

async def adding_vk_token(message: Message):
    
    logging.debug(f"user {message.from_id} join in 'adding_vk_token' function")

    sql.set_group_value(group_id, "VK_TOKEN", message.text)
    
    sql.set_tg_user_status(message.from_id, "adding vk wall token")

    await message.answer("Введите токен вк с правами управления постами:")

async def adding_vk_wall_token(message: Message):

    logging.debug(f"user {message.from_id} join in 'adding_vk_wall_token' function")

    sql.set_group_value(group_id, "VK_TOKEN_FOR_DELAY", message.text)

    sql.set_tg_user_status(message.from_id, "adding vk admin")

    await message.answer("Пришлите id пользователя вконтакте, который будет администратором чат бота:")

async def adding_vk_admin(message: Message):
    
    logging.debug(f"user {message.from_id} join in 'adding_vk_admin' function")

    sql.add_vk_admin(group_id, message.text)

    sql.set_tg_user_status(message.from_id, "None")

    group = Group(group_id)
    server.add_group(group)
    
    try:
        group.init()
        await message.answer("Группа добавлена!", reply_markup=admin_panel_keyboard(message.from_id))
    except:
        await message.answer("Не удалось запустить чат-бота, проверьте данные и добавьте группу заново")
        server.remove_group(group.GROUP_NAME)


def register_adding_group_handlers(dp: Dispatcher):

    dp.register_message_handler(add_group, isUser() & Text(equals="Добавить группу"))
    dp.register_message_handler(adding_group_id, isAddingGroupID() & isNoCurrentGroup())
    dp.register_message_handler(adding_group_name, isAddingGroupName() & isNoCurrentGroup())
    dp.register_message_handler(adding_vk_token, isAddingVkToken() & isNoCurrentGroup())
    dp.register_message_handler(adding_vk_wall_token, isAddingVkWallToken() & isNoCurrentGroup())
    dp.register_message_handler(adding_vk_admin, isAddingVkAdmin() & isNoCurrentGroup())
