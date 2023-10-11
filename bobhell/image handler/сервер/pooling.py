import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from aiogram.utils import executor
import image_handler
from io import BytesIO
from aiogram.types import InputMediaPhoto
from PIL import Image
import time


API_TOKEN = '6516087703:AAFogf1wdiNFFkolsNWMjOvSXj0BN3ypi5g'  # рабочий токен бота для выдачи фото

admins = [1020541698, 6356732052]

on_off = "Off"
#условный текстовый массив
threads = []

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
    """
    Обработчик команды /start.
    Отправляет приветственное сообщение.
    """
    if on_off == "On" or admin(message.from_id):

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        # Добавляем кнопки
        button1 = types.KeyboardButton("Получить фото (Франция)")
        button2 = types.KeyboardButton("Получить фото (Испания)")

        keyboard.add(button1)
        keyboard.add(button2)
        # Отправляем сообщение с клавиатурой
        await message.answer(text="Бим бим бам бам", reply_markup=keyboard)

    else:
        await message.answer("Бот временно остановлен администратором")

@dp.message_handler(commands=['count'])
async def count(message: Message):
    if on_off == "On" or admin(message.from_id):
        with open(image_handler.backgrounds_list, 'r') as file:
            # Прочитайте строки из файла и создайте массив ссылок
            links = [line.strip() for line in file]

        await message.answer(text=len(links))
    else:
        await message.answer("Бот временно остановлен администратором")

@dp.message_handler(lambda message: message.text == 'Получить фото (Франция)')
async def get_photo(message: Message):

    
    if on_off == "On" or admin(message.from_id):
        if len(threads) > 10:

            await message.answer("Большая нагрузка на бота, попробуйте позже!")
        else:

            threads.append("thread")
            
            images = image_handler.start_combine(country="FRANCE")

            if images:

                input_media_images = []
                
                i = 0

                while i < len(images) - 1:
                    image_stream = BytesIO()
                    images[i].save(image_stream, format='JPEG')
                    image_stream.seek(0)
                    input_media_images.append(InputMediaPhoto(media=image_stream)) 
                    i = i + 1   
                print("Фото сгенерированы!")

            await message.answer_media_group(media = input_media_images)
            threads.pop()

    else:
        await message.answer("Бот временно остановлен администратором")
    
@dp.message_handler(lambda message: message.text == 'Получить фото (Испания)')
async def get_photo(message: Message):

    
    if on_off == "On" or admin(message.from_id):
        if len(threads) > 10:

            await message.answer("Большая нагрузка на бота, попробуйте позже!")
        else:

            threads.append("thread")
            
            images = image_handler.start_combine(country="SPAIN")

            if images:

                input_media_images = []
                
                i = 0

                while i < len(images) - 1:
                    image_stream = BytesIO()
                    images[i].save(image_stream, format='JPEG')
                    image_stream.seek(0)
                    input_media_images.append(InputMediaPhoto(media=image_stream)) 
                    i = i + 1   
                print("Фото сгенерированы!")

            await message.answer_media_group(media = input_media_images)
            threads.pop()

    else:
        await message.answer("Бот временно остановлен администратором")

@dp.message_handler(commands=['help'])
async def on_start(message: Message):

    if admin(message.from_id):
        await message.answer(text="stop - остановка бота\n"+
                                    "start - запуск бота\n"
                                    "add (id) - добавление админа\n"
                                    "(текстовый документ) - добавление списка фонов\n"
                                    "(группа фотографий) - изменение фото\n"
                                    "/help - список функций админ-панели")

# Обработчик приема документа
@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def process_document(message: types.Message):
    global on_off
    try:
        #добавление списка фонов
        if admin(message.from_id):
            on_off = "Off"
            time.sleep(10)
            # Скачиваем документ
            file_path = await bot.get_file(message.document.file_id)
            document = await bot.download_file(file_path.file_path)

            # Извлекаем текст из загруженного документа
            document_bytes = document.read()
            new_backgrounds = document_bytes.decode("utf-8")      
            new_backgrounds = new_backgrounds.replace("\r", "") 

            with open(image_handler.backgrounds_list, "a") as file:
                # Добавляем новый текст с новой строкой
                file.write("\n"+ new_backgrounds)   

            on_off = "On"
            await message.answer(text="Фоны успешно добавлены!")
    except:
        await message.answer("Произошла ошибка")
"""
@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def process_photos(message: types.Message):

    try:
        if admin(message.from_id):

            on_off = "Off"
            #time.sleep(10)
            #удаляем старые фото
            image_handler.clear_overlays()

            # Скачиваем и сохраняем новые фотографии
            for i, photo in enumerate(message.photo):
                file_id = photo.file_id
                file_path = await bot.get_file(file_id)
                file_name = f"{i+1}.jpg"  # Имя файла, например, "1.jpg", "2.jpg" и так далее
                downloaded_photo = await bot.download_file(file_path.file_path)
                with open(os.path.join(image_handler.overlay_folder, file_name), "wb") as file:
                    file.write(downloaded_photo.read())

            #on_off = "On"
            await message.answer(text="Фото успешно изменены!")
    except:
        await message.answer("Произошла ошибка")
"""
@dp.message_handler()
async def echo(message: Message):
    global footage
    global on_off
    try:
        if admin(message.from_id):

            #добавление администратора
            if "add" in message.text:
                admin_id = int(message.text.split(" ")[1])
                admins.append(admin_id)
                await message.answer(f"Добавлен администратор с id: {admin_id}")

            #остановка бота
            elif message.text == "stop":
                if on_off == "On":
                    on_off = "Off"
                    await message.answer("Остановка бота")
                else:
                    await message.answer("Бот уже остановлен")

            #запуск бота
            elif message.text == "start":
                if on_off == "Off":
                    on_off = "On"
                    await message.answer("Запуск бота")
                else:
                    await message.answer("Бот уже запущен")

            #статус
            elif message.text == "status":
                
                await message.answer(on_off)

            return
            
    except: 
        await message.answer(text="Попробуйте позже")


def main():
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()