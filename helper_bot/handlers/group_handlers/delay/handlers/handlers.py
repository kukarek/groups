from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from database import sql
import logging
from ..keyboards import *
from ..filters import *
from misc import server 


async def start(message: Message):

    logging.debug(f"user {message.from_id} join in 'start' function")
    
    group = server.get_group(sql.get_current_group_id(message.from_id))

    await message.answer("Редактирование параметров отложки..", reply_markup=edit_delay_keyboard(group))

async def edit_date(message: Message):

    logging.debug(f"user {message.from_id} join in 'edit_date' function")

    group = server.get_group(sql.get_current_group_id(message.from_id))

    sql.set_tg_user_status(message.from_id, "setting date")

    await message.answer("Выберите дату..", reply_markup=choose_date_keyboard())

async def editing_date(message: Message):

    logging.debug(f"user {message.from_id} join in 'editing_date' function")

    group = server.get_group(sql.get_current_group_id(message.from_id))

    group.set_date(message.text)

    sql.set_tg_user_status(message.from_id, "None")

    await message.answer(f"Устанавливаю отложку на {message.text.lower()}", reply_markup=edit_delay_keyboard(group))

async def edit_start_time(message: Message):

    logging.debug(f"user {message.from_id} join in 'edit_start_time' function")
    sql.set_tg_user_status(message.from_id, "setting start hour")

    await message.answer("Введите одной цифрой час, с котого будет собрана отложка..")

async def editing_start_time(message: Message):

    logging.debug(f"user {message.from_id} join in 'editing_start_time' function")
    
    group = server.get_group(sql.get_current_group_id(message.from_id))
    if group.set_start_hour(message.text):

        sql.set_tg_user_status(message.from_id, "None")

        await message.answer(f"Время старта: {message.text}:00")

    else:
        await message.answer(f"Некорректное время, введите еще раз:")

async def edit_end_time(message: Message):

    logging.debug(f"user {message.from_id} join in 'edit_end_time' function")

    sql.set_tg_user_status(message.from_id, "setting end hour")

    await message.answer("Введите одной цифрой час, до которого будет собрана отложка..")
    
async def editing_end_time(message: Message):

    logging.debug(f"user {message.from_id} join in 'editing_end_time' function")

    group = server.get_group(sql.get_current_group_id(message.from_id))

    if group.set_end_hour(message.text):

        sql.set_tg_user_status(message.from_id, "None")

        await message.answer(f"Время завершения: {message.text}:00")

    else:
        await message.answer(f"Некорректное время, введите еще раз:")

async def start_parsing(message: Message):

    logging.debug(f"user {message.from_id} join in 'start_parsing' function")

    group = server.get_group(sql.get_current_group_id(message.from_id))
    posts = group.get_posts()

    for post in posts:
        logging.debug(f"bot send {message.from_id} parsed {post.text}")
        mess = await message.answer(post.text)
        await mess.edit_reply_markup(inline_keyboard(chat_id=message.from_id, message_id=mess.message_id, post=post))

    await message.answer(f"Количество постов: {len(posts)}", reply_markup=on_start_keyboard())

async def make_delay(message: Message):
    
    logging.debug(f"user {message.from_id} join in 'make_delay' function")

    group = server.get_group(sql.get_current_group_id(message.from_id))
    if group.make_def():

        await message.answer("Отложка создана!")
    else:
        await message.answer("Произошла ошибка :(")

async def change_parsers(message: Message):

    logging.debug(f"user {message.from_id} join in 'change_parsers' function")
    await message.answer("Изменение парсеров...", reply_markup=editing_parsers_keyboard())

async def add_parser(message: Message):

    logging.debug(f"user {message.from_id} join in 'add_parser' function")
    sql.set_tg_user_status(message.from_id, "additing parser")
    await message.answer("Отправьте ссылку на тг канал (https://t.me/channel)")

async def additing_parser(message: Message):

    logging.debug(f"user {message.from_id} join in 'additing_parser' function")
    sql.set_tg_user_status(message.from_id, "None")
    group = server.get_group(sql.get_current_group_id(message.from_id))
    group.add_channel_parser(message.text)
    await message.answer("Парсер добавлен!", reply_markup=editing_parsers_keyboard())

async def remove_parser(message: Message):

    logging.debug(f"user {message.from_id} join in 'remove_parser' function")
    sql.set_tg_user_status(message.from_id, "removing parser")
    group = server.get_group(sql.get_current_group_id(message.from_id))
    await message.answer("Выберите парсер:", reply_markup=delete_parser_keyboard(group))

async def removing_parser(message: Message):

    logging.debug(f"user {message.from_id} join in 'removing_parser' function")
    sql.set_tg_user_status(message.from_id, "None")
    remove_parser(message.text)
    await message.answer("Парсер удален!", reply_markup=editing_parsers_keyboard())

async def cancel(message: Message):

    logging.debug(f"user {message.from_id} join in 'cancel' function")

    group = server.get_group(sql.get_current_group_id(message.from_id))
    group.remove_all_post()
    await message.answer("Меню:", reply_markup=edit_delay_keyboard(group))

async def remove_post(query: CallbackQuery):

    logging.debug(f"user {query.message.from_id} join in 'remove_post' function")

    chat_id = int(query.data.split("_")[1])
    message_id = int(query.data.split("_")[2])
    post_id =  int(query.data.split("_")[3])

    group = server.get_group(sql.get_current_group_id(chat_id))
    group.remove_post(post_id)
    await query.bot.delete_message(chat_id=chat_id, message_id=message_id)

async def edit_default_photo(message: Message):

    sql.set_tg_user_status(message.from_id, "editing default photo")

    await message.answer("Отправьте фотографию из вк альбома в формате photo-22156807_457244649 (показывается в url при нажатии на фото в альбоме)")

async def editing_default_photo(message: Message):

    sql.set_tg_user_status(message.from_id, "None")
    group = server.get_group(sql.get_current_group_id(message.from_id))
    if group.set_default_photo(message.text):

        await message.answer("Фотография установлена!", reply_markup=edit_delay_keyboard(group))
    else:
        await message.answer("Фотография не найдена :(", reply_markup=edit_delay_keyboard(group))

def register_delay_handlers(dp: Dispatcher):

    dp.register_message_handler(start, Text(equals="Отложка") & isUser())
    dp.register_message_handler(edit_date, Text(equals="Дата") & isUser())
    dp.register_message_handler(editing_date, IsSettingDate() & Text(equals="Завтра"))
    dp.register_message_handler(editing_date, IsSettingDate() & Text(equals="Сегодня"))
    dp.register_message_handler(edit_start_time, Text(equals="Время начала") & isUser())
    dp.register_message_handler(edit_end_time, Text(equals="Время завершения") & isUser())
    dp.register_message_handler(start_parsing, Text(equals="Начать парсинг") & isUser())
    dp.register_message_handler(change_parsers, Text(equals="Изменить парсеры") & isUser())
    dp.register_message_handler(change_parsers, Text(equals="Добавить парсеры") & isUser())
    dp.register_message_handler(add_parser, Text(equals="Добавить парсер тг") & isUser())
    dp.register_message_handler(remove_parser, Text(equals="Удалить парсер") & isUser())
    dp.register_message_handler(start, Text(equals="Меню") & isUser())

    dp.register_message_handler(make_delay, Text(equals="Сделать отложку") & isUser())
    dp.register_message_handler(cancel, Text(equals="Отменить изменения") & isUser())

    dp.register_callback_query_handler(remove_post, lambda query: query.data.startswith("remove"))

    dp.register_message_handler(edit_default_photo, Text(equals="Добавить фото по умолчанию (посты с тг выкладываются без фото)") & isExistCurrentGroup())
    dp.register_message_handler(edit_default_photo, Text(equals="Изменить фото для постов") & isExistCurrentGroup())
    dp.register_message_handler(editing_default_photo, isEditingDefaultPhoto() & isExistCurrentGroup())

    dp.register_message_handler(editing_start_time, IsSettingStartHour())
    dp.register_message_handler(editing_end_time, IsSettingEndHour())
    dp.register_message_handler(additing_parser, IsAdditingParser())
    dp.register_message_handler(removing_parser, IsRemovingParser())