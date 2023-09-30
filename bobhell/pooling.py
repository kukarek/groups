import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
import threading


API_TOKEN = '6687202213:AAEl9SKJN-9xPPE37A3Z5WEYLMfZlKtTI1Y'  # Замените YOUR_TELEGRAM_BOT_TOKEN на ваш токен

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def on_start(message: Message):
    """
    Обработчик команды /start.
    Отправляет приветственное сообщение.
    """
    await message.answer("Привет! Я бот. Напиши мне что-нибудь!")

def main():
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()

    
