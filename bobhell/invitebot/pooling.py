import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from aiogram.utils import executor
import threading
import asyncio


API_TOKEN = '6234772391:AAH1Vow3gIGerfwmzfxjoSaKpGXYakBvZdg'  # Замените YOUR_TELEGRAM_BOT_TOKEN на ваш токен

admins = [1020541698, 6108609160]

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)


# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def admin(id):
    for admin in admins:
        if admin == id:
            return True
    return False

@dp.message_handler(commands=['start'])
async def on_start(message: Message):
    
    print()
    
    



@dp.message_handler()
async def echo(message: Message):
    
    print()


def main():
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()
    
