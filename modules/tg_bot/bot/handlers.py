from ...vk_bot.bot.main import vk
from log.loggHandler import ERROR
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from ..functions import vk_top
from ..functions import wrapping
from misc.config import GROUPKZN_ID, GROUPKZN_LINK
from aiogram.types import Message
import logging
from .filters import *
from .keyboards import *
from ..functions.wrapping.states import wrapping
from ..functions.wrapping import handler


logg = logging.getLogger(__name__)
logg.addHandler(ERROR(vk=vk))

async def on_start(message: Message):

    logg.debug(f"user {message.from_id} join in 'on_start' function")
    await message.answer("Добро пожаловать в helper bot!", reply_markup=admin_panel_keyboard())

async def get_top(message: Message):
    
    logg.debug(f"user {message.from_id} join in 'get_top' function")

    topkzn = vk_top.Get_top(url = GROUPKZN_LINK, group_id = GROUPKZN_ID)

    await message.answer(f"Место в топе по Казани: {topkzn}")

async def balance(message: Message):
    
    logg.debug(f"user {message.from_id} join in 'balance' function")

    try:
        balance = handler.get_balance()
        await message.answer(f"Текущий баланс: {balance}")
    except Exception as e:
        logg.error(e)

async def status(message: Message):

    logg.debug(f"user {message.from_id} join in 'status' function")

    try:
        await message.answer(wrapping.status(), reply_markup=wrapping_state_panel_keyboard())
    except Exception as e:
        logg.error(e)
    
async def stop_wrapping(message: Message):
    
    logg.debug(f"user {message.from_id} stopped wrapping")
    wrapping.stop()
    
    await message.answer("Накрутка остановлена!")

async def wrapping_panel(message: Message):
    
    logg.debug(f"user {message.from_id} in wrapping panel")
    await message.answer("Панель накруки", reply_markup=wrapping_panel_keyboard())

async def on_start_wrapping(message: Message):

    logg.debug(f"user {message.from_id} on start wrapping")
    
    await message.answer("Выберите параметры:", reply_markup=wrapping_start_panel_keyboard())

async def start_wrapping(message: Message):

    logg.debug(f"user {message.from_id} started wrapping")
    wrapping.start()
    await message.answer(f"Накрутка запущена!\n {wrapping.status()}")

async def change_tg(message: Message):

    logg.debug(f"user {message.from_id} change tg")
    wrapping.change_TG()

    await message.answer("Изменения приняты!", reply_markup=wrapping_start_panel_keyboard())

async def change_vk(message: Message):

    logg.debug(f"user {message.from_id} change vk")
    wrapping.change_VK()

    await message.answer("Изменения приняты!", reply_markup=wrapping_start_panel_keyboard())

async def cycle(message: Message):

    logg.debug(f"user {message.from_id} set cycle")
    mini_db[message.from_id] = "setting cycle"

    await message.answer("Введите цикл от 0 до 27 цифрой")

async def setting_cycle(message: Message):

    logg.debug(f"user {message.from_id} entered cycle: {message.text}")

    mini_db[message.from_id] = None
    wrapping.cycle = int(message.text)

    await message.answer("Изменения приняты!")

async def timer(message: Message):

    logg.debug(f"user {message.from_id} set timer")
    mini_db[message.from_id] = "setting timer"

    await message.answer("Введите количество минут (цифрой) для отложенного запуска накрутки")

async def setting_timer(message: Message):

    logg.debug(f"user {message.from_id} entered timer value: {message.text}")

    mini_db[message.from_id] = None
    wrapping.timer = int(message.text)

    await message.answer("Изменения приняты!")

async def send_log(message: Message):

    with open('log/log.log', 'rb') as log_file:
        await message.answer_document(document=log_file)


def register_all_handlers(dp: Dispatcher):

    dp.register_message_handler(on_start, commands=['start'])
    dp.register_message_handler(get_top, Text(equals="Получить топ"))
    dp.register_message_handler(balance, Text(equals="Баланс"))
    dp.register_message_handler(status, Text(equals="Состояние накрутки"))
    dp.register_message_handler(stop_wrapping, Text(equals="Остановить накрутку"))
    dp.register_message_handler(wrapping_panel, Text(equals="Накрутка"))
    dp.register_message_handler(on_start_wrapping, Text(equals="Запустить накрутку"))
    dp.register_message_handler(change_tg, (Text(equals="Отключить телеграм") | Text(equals="Включить телеграм")))
    dp.register_message_handler(change_vk, (Text(equals="Отключить вк") | Text(equals="Включить вк")))
    dp.register_message_handler(cycle, Text(equals="Цикл"))
    dp.register_message_handler(setting_cycle, isSettingCycle())

    dp.register_message_handler(start_wrapping, Text(equals="Запустить"))

    dp.register_message_handler(timer, Text(equals="Таймер"))
    dp.register_message_handler(setting_timer, isSettingTimer())

    dp.register_message_handler(on_start, Text(equals="Главное меню"))

    dp.register_message_handler(send_log, commands=("log"))