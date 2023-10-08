import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from aiogram.utils import executor
import asyncio
import chatbot_logic
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import sql

API_TOKEN = '6234772391:AAH1Vow3gIGerfwmzfxjoSaKpGXYakBvZdg'  # Замените YOUR_TELEGRAM_BOT_TOKEN на ваш токен

admin = 6108609160

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)


# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


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
 
    await bot.delete_message(chat_id=admin, message_id=message_id)
    await bot.send_message(chat_id=user_id, text="Ваша заявка принята!\n\n"+
                                                 "Чат - https://t.me//+7w7nKlAJFEA2NGM1")
    

@dp.callback_query_handler(lambda query: query.data.startswith("reject_"))
async def on_button2_click(query: CallbackQuery):
    
    user_id = int(query.data.split("_")[1]) #от кого заявка
    message_id = int(query.data.split("_")[2]) #id сообщения у админа
 
    await bot.delete_message(chat_id=admin, message_id=message_id)
    await bot.send_message(chat_id=user_id, text="Ваша заявка отклонена!")
    
@dp.message_handler()
async def echo(message: Message):
    
    if message.from_id == admin:
        return

    response, notify = chatbot_logic.reply_message_handler(user_id=message.from_id, message_text=message.text)

    if response != None:
        await message.answer(text=response)
    
    if notify != None:

        mess = await bot.send_message(chat_id=admin, text=notify)
        keyboard = generate_inline_keyboard(user_id=message.from_id, message_id=mess.message_id)
        await bot.edit_message_reply_markup(chat_id=admin, message_id=mess.message_id, reply_markup=keyboard)

def main():
    # Запуск бота
    sql.create_connection()
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()
    
