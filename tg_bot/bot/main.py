import logging
from aiogram import Bot, Dispatcher, executor
from . import register_all_handlers

from misc.config import API_TOKEN

async def on_start(dp: Dispatcher):
    
    register_all_handlers(dp)

def start_bot():
    # Установка уровня логирования
    logging.basicConfig(level=logging.INFO)

    # Инициализация бота и диспетчера
    bot = Bot(token=API_TOKEN["helper"])
    dp = Dispatcher(bot)

    # Запуск бота
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)


if __name__ == '__main__':
    start_bot()
    
