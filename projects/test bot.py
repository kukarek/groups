import asyncio
from aiogram import Bot, Dispatcher, types
import requests

API_TOKEN = '6470735932:AAHG7LzA_VtGZvmK5JopIMqoiNa3CmuEvuM'  # Укажите здесь ваш токен API (TG) API_TOKEN = '6588918438:AAEuWOePbDIWlDufBsnHTku9wj9oHlU5IrQ'
API_KEY = "bb8cad79840056d1fff7676360a48b97" # токен PROSMMTOP
API_URL = "https://prosmmtop.ru/api/v2"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я буду считывать ID новых сообщений на канале.")

# Обработчик всех входящих сообщений на канале
@dp.channel_post_handler(content_types=types.ContentTypes.ANY)
async def handle_channel_post(message: types.Message):
    message_id = message.message_id  # ID нового сообщения
   
    message_url = f"https://t.me/rabotachelyabinski/{message_id}"  #накрут последнего сообщения
    params = dict(key=API_KEY, action="add", service=614, link=message_url, quantity=500)
    res = requests.get(API_URL, params=params)
    print(f"tg {str(res.json())}")
   
    previous_message_url = f"https://t.me/rabotachelyabinski/{message_id - 1}"   #накрут предпоследнего сообщения
    params = dict(key=API_KEY, action="add", service=614, link=previous_message_url, quantity=500)
    res = requests.get(API_URL, params=params)
    print(f"tg {str(res.json())}")



if __name__ == '__main__':

    print("привет")
    from aiogram import executor
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, skip_updates=True, loop=loop)
