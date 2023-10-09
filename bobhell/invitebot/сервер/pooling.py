import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from aiogram.utils import executor
import asyncio
import chatbot_logic
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import sql
from bs4 import BeautifulSoup
import requests

API_TOKEN = '6234772391:AAH1Vow3gIGerfwmzfxjoSaKpGXYakBvZdg'  # Замените YOUR_TELEGRAM_BOT_TOKEN на ваш токен

admin = 6108609160
owner = 1020541698
channel = -1001821448494
# Установка уровня логирования
logging.basicConfig(level=logging.INFO)


# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def get_usd_exchange_rate():
    url = 'https://www.cbr.ru/currency_base/daily/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        html = response.text
        # Создаем объект BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Находим все строки (элементы <tr>) в таблице
        rows = soup.find_all('tr')
        # Извлечение курса доллара

        # Проходим по строкам и ищем курс доллара
        usd_rate = None

        for row in rows:
            # Находим все ячейки (элементы <td>) в текущей строке
            cells = row.find_all('td')
            
            # Проверяем, что есть хотя бы 5 ячеек (с учетом столбца "Курс")
            if len(cells) >= 5:
                # Проверяем, что буквенный код валюты (вторая ячейка) равен "USD"
                if cells[1].text.strip() == "USD":
                    usd_rate = cells[4].text.strip()
                    break  # Нашли курс доллара, выходим из цикла
        
        return usd_rate
    except:
        return None

def generate_inline_keyboard(user_id, message_id):

    button1 = InlineKeyboardButton("Принять", callback_data=f"accept_{user_id}_{message_id}") 
    button2 = InlineKeyboardButton("Отклонить", callback_data=f"reject_{user_id}_{message_id}") 

    keyboard = InlineKeyboardMarkup()
    keyboard.row(button1, button2)
    return keyboard
    
@dp.callback_query_handler(lambda query: query.data.startswith("accept_"))
async def on_button1_click(query: CallbackQuery):
    
    user_id = int(query.data.split("_")[1]) #от кого заявка
    message_id = int(query.data.split("_")[2]) #id сообщения у админа
 
    await bot.delete_message(chat_id=channel, message_id=message_id)
    await bot.send_message(chat_id=user_id, text="Ваша заявка принята!\n\n"+
                                                 "Чат - https://t.me/+tkdRMOFp6MYwMTY1")
    

@dp.callback_query_handler(lambda query: query.data.startswith("reject_"))
async def on_button2_click(query: CallbackQuery):
    
    user_id = int(query.data.split("_")[1]) #от кого заявка
    message_id = int(query.data.split("_")[2]) #id сообщения у админа
 
    await bot.delete_message(chat_id=channel, message_id=message_id)
    await bot.send_message(chat_id=user_id, text="Ваша заявка отклонена!")

@dp.message_handler(commands=['test'])
async def on_start(message: Message):

    if message.from_id == owner or message.from_id == channel:
        await message.answer("Все работает")
 
@dp.channel_post_handler()
async def echo(message: Message):
    if message.text == "test":
        await message.answer("Все работает")
    else:
        try:
            rub = float(message.text)
            course = float(get_usd_exchange_rate().replace(",", "."))
            usd = rub / course
            await message.answer(f"{round(usd, 2)} USD")
        except Exception as e:
            await message.answer(f"Ошибочка где-то...\n\n {e}")

@dp.message_handler()
async def echo(message: Message):
    
    if message.from_id == channel:
        return

    response, notify = chatbot_logic.reply_message_handler(user_id=message.from_id, message_text=message.text)

    if response != None:
        await message.answer(text=response)
    
    if notify != None:

        mess = await bot.send_message(chat_id=channel, text=notify)
        keyboard = generate_inline_keyboard(user_id=message.from_id, message_id=mess.message_id)
        await bot.edit_message_reply_markup(chat_id=channel, message_id=mess.message_id, reply_markup=keyboard)

def main():
    # Запуск бота
    sql.create_connection()
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()
    

