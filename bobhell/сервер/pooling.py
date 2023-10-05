import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from aiogram.utils import executor
import threading
import image_handler
from io import BytesIO
from aiogram.types import InputMediaPhoto
from PIL import Image


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
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    # Добавляем кнопки
    button1 = types.KeyboardButton("Получить фото")
    keyboard.add(button1)
    # Отправляем сообщение с клавиатурой
    await message.answer(text="Бим бим бам бам", reply_markup=keyboard)

@dp.message_handler(commands=['count'])
async def count(message: Message):

    with open(image_handler.backgrounds_list, 'r') as file:
        # Прочитайте строки из файла и создайте массив ссылок
        links = [line.strip() for line in file]

    await message.answer(text=len(links))

@dp.message_handler(lambda message: message.text == 'Получить фото')
async def get_photo(message: Message):

    try:
        images = image_handler.start_combine()

        if images:

            input_media_images = []
            
            i = 0
            
            while i < len(images) - 1:
                image_stream = BytesIO()
                images[i].save(image_stream, format='JPEG')
                image_stream.seek(0)
                input_media_images.append(InputMediaPhoto(media=image_stream)) 
                i = i + 1   
            
            print("Фото отправлены!")
            await message.answer_media_group(media = input_media_images) 
    except:
        await message.answer(text="Попробуйте позже")

def main():
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()

    
