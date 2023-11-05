from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
import logging
from database import sql
from misc import server 
from ..filters import *
from ..keyboards import *

async def edit_group_param(message: Message):

    await message.answer("Редактирование группы...", reply_markup=group_parameters_keyboard(message.from_id))

async def add_vk_admin(message: Message):

    sql.set_tg_user_status(message.from_id, "adding vk admin")

    await message.answer("Введите id администратора вк:")

async def adding_vk_admin(message: Message):

    sql.set_tg_user_status(message.from_id, "None")
    group = server.get_group(sql.get_current_group_id(message.from_id))
    sql.add_vk_admin(group.GROUP_ID, message.text)

    await message.answer("Администратор добавлен!", reply_markup=group_parameters_keyboard(message.from_id))

async def remove_vk_admin(message: Message):

    sql.set_tg_user_status(message.from_id, "removing vk admin")
    group = server.get_group(sql.get_current_group_id(message.from_id))
    admins = sql.get_vk_admins(group.GROUP_ID)

    await message.answer("Выберите администратора", reply_markup=admins_for_remove_keyboard(admins))

async def removing_vk_admin(message: Message):
    
    group_id = sql.get_current_group_id(message.from_id)
    sql.set_tg_user_status(message.from_id, "None")
    if sql.remove_vk_admin(group_id, message.text):

        await message.answer("Администратор удален", reply_markup=group_parameters_keyboard(message.from_id))

    else:
        await message.answer("Неверный id")

async def cancel(message: Message):

    await message.answer("Редактирование группы...", reply_markup=group_parameters_keyboard(message.from_id))

async def edit_rules_link(message: Message):

    sql.set_tg_user_status(message.from_id, "editing rules link")

    await message.answer("Пришлите ссылку на статью с правилами размещения:")

async def editing_rules_link(message: Message):

    sql.set_tg_user_status(message.from_id, "None")
    group = server.get_group(sql.get_current_group_id(message.from_id))
    group.RULES_LINK = message.text

    await message.answer("Ссылка изменена!", reply_markup=group_parameters_keyboard(message.from_id))

async def edit_example_words(message: Message):

    sql.set_tg_user_status(message.from_id, "editing example words")

    await message.answer("Пришлите пример слов для подписки:")

async def editing_example_words(message: Message):

    sql.set_tg_user_status(message.from_id, "None")
    group = server.get_group(sql.get_current_group_id(message.from_id))
    group.EXAMPLE_WORDS = message.text

    await message.answer("Слова изменены!", reply_markup=group_parameters_keyboard(message.from_id))

async def edit_search_words(message: Message):

    sql.set_tg_user_status(message.from_id, "editing search words")

    await message.answer("Пришлите пример слов для подписки:")

async def editing_search_words(message: Message):

    sql.set_tg_user_status(message.from_id, "None")
    group = server.get_group(sql.get_current_group_id(message.from_id))
    group.SEARCH_KEYWORDS = message.text

    await message.answer("Слова изменены!", reply_markup=group_parameters_keyboard(message.from_id))

async def edit_payment(message: Message):

    sql.set_tg_user_status(message.from_id, "editing payment")

    await message.answer("Отправьте текстом ваши реквизиты:")

async def editing_payment(message: Message):

    sql.set_tg_user_status(message.from_id, "None")
    group = server.get_group(sql.get_current_group_id(message.from_id))
    group.PAYMENT = message.text

    await message.answer("Реквизиты изменены!", reply_markup=group_parameters_keyboard(message.from_id))

def register_group_param_handlers(dp: Dispatcher):
    
    dp.register_message_handler(edit_group_param, Text(equals="Редактировать") & isExistCurrentGroup())

    dp.register_message_handler(add_vk_admin, Text(equals="Добавить админа") & isExistCurrentGroup())
    dp.register_message_handler(adding_vk_admin, isAddingVkAdmin() & isExistCurrentGroup())

    dp.register_message_handler(remove_vk_admin, Text(equals="Удалить админа") & isExistCurrentGroup())
    dp.register_message_handler(cancel, Text(equals="Отмена") & isRemovingVkAdmin())
    dp.register_message_handler(removing_vk_admin, isRemovingVkAdmin() & isExistCurrentGroup())

    dp.register_message_handler(edit_rules_link, Text(equals="Изменить правила размещения") & isExistCurrentGroup())
    dp.register_message_handler(editing_rules_link, isEditingRulesLink())

    dp.register_message_handler(edit_example_words, Text(equals="Изменить пример слов") & isExistCurrentGroup())
    dp.register_message_handler(editing_example_words, isEditingExampleWords() & isExistCurrentGroup())

    dp.register_message_handler(edit_search_words, Text(equals="Изменить слова для поиска топа") & isExistCurrentGroup())
    dp.register_message_handler(editing_search_words, isEditingSearchWords() & isExistCurrentGroup())

    dp.register_message_handler(edit_payment, Text(equals="Изменить способы оплаты") & isExistCurrentGroup())
    dp.register_message_handler(editing_payment, isEditingPayment() & isExistCurrentGroup())

    