import logging
import log
from aiogram import Bot, Dispatcher, executor
from misc.config import API_TOKEN
from misc import server 
from .handlers.main_handlers import register_all_handlers
from database import sql

bot = Bot(token=API_TOKEN["helper_test"])
main_logger = logging.getLogger("main_log")

async def init(dp: Dispatcher):

    log.init("DEBUG")
    sql.create_connection()
    
    server.groups_init()
    register_all_handlers(dp)

    logging.debug("Все модули зарегистрированы, запускается пулинг!")


def start_bot():

    dp = Dispatcher(bot)
    # Запуск бота
    executor.start_polling(dp, skip_updates=True, on_startup=init)


