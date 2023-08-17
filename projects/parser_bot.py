import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
import parservk
import threading
import wrapping

group_id_chlb = "220670949"
url_chlb = "https://vk.com/search?c%5Bper_page%5D=40&c%5Bq%5D=%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%20%D1%87%D0%B5%D0%BB%D1%8F%D0%B1%D0%B8%D0%BD%D1%81%D0%BA&c%5Bsection%5D=communities"

group_id_kzn = "22156807"
url_kzn = "https://vk.com/search?c%5Bper_page%5D=40&c%5Bq%5D=%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%20%D0%BA%D0%B0%D0%B7%D0%B0%D0%BD%D1%8C&c%5Bsection%5D=communities"

API_TOKEN = '6576254488:AAHYcpkpwlONZUlDR6JuB1_MYI-RTSWunEo'  # Замените YOUR_TELEGRAM_BOT_TOKEN на ваш токен

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


@dp.message_handler(commands=['get_top'])
async def on_start(message: Message):
   
    topchlb = parservk.Get_top(url = url_chlb, group_id = group_id_chlb)
    topkzn = parservk.Get_top(url = url_kzn, group_id = group_id_kzn)

    await message.answer(f"Место в топе по Челябинску: {topchlb}\n"
                         f"Место в топе по Казани: {topkzn}")
    


@dp.message_handler(commands=['help'])
async def on_help(message: Message):
    """
    Обработчик команды /help.
    Отправляет справку по использованию бота.
    """
    await message.answer("Я - простой бот, который отвечает на команды. "
                         "Доступные команды:\n"
                         "/start - Начать общение с ботом\n"
                         "/help - Получить справку\n"
                         "/get_top - получить номер в поиске")

@dp.message_handler(commands=['start_wrapping'])
async def on_help(message: Message):
    
    wrapping.start_wrapping()
    


@dp.message_handler()
async def echo(message: Message):
    """
    Обработчик всех остальных сообщений.
    Просто повторяет сообщение обратно.
    """
    await message.answer(f"Вы написали: {message.text}")

def main():
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()

    
