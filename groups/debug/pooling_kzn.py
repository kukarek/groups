import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import asyncio
import aiogram
import time
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import subscriber
from config import VK_TOKEN, TELEGRAM_TOKEN, CHANNEL_ID, GROUPKZN_ID, ADMIN

# Инициализация Telegram бота
async def send_telegram(image, caption):
    
    bot = Bot(token=TELEGRAM_TOKEN)
    
    if image=="":
      
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=caption)

        except aiogram.utils.exceptions.BadRequest as e:
      
            print(f"Error sending text(казань): {e}")
    else:
        try:
            await bot.send_photo(chat_id=CHANNEL_ID, photo=image, caption=caption)

        except aiogram.utils.exceptions.BadRequest as e:
            print(f"Error sending media group(казань): {e}")

    await bot.close()

def send_to_telegram(event):
   
    message = event.object.text
    if len(message) < 4000:
        if len(message) < 1000:

            attachments = event.object.attachments

            if attachments and "photo" in attachments[0]:
                # Если в записи есть изображения, получаем ссылку на изображение
                photo_url = attachments[0]["photo"]["sizes"][-1]["url"]
                asyncio.run(send_telegram(image=photo_url, caption=message))
            else:
                # Если в записи нет изображений, отправляем только текст
                asyncio.run(send_telegram(image= "", caption=message))
        else:
            asyncio.run(send_telegram(image= "", caption=message))  

def main():
    
    while True:
        
        vk_session = vk_api.VkApi(token=VK_TOKEN)
        longpoll = VkBotLongPoll(vk_session, GROUPKZN_ID)  
        vk = vk_session.get_api()

        print("соединение установлено- казань")

        try:
           
            for event in longpoll.listen():
             
                if event.type == VkBotEventType.MESSAGE_NEW:
                    #id группы = event.group_id
                    reply, keybord, notify = subscriber.reply_message_handler(event=event)

                    if notify == True: #уведомление админа
                        vk.messages.send(user_id=ADMIN, message=f"Новое сообщение! '{event.message.text}'", random_id=0)
                        
                    if reply != None: #отправка ответа юзеру с клавиатурой, либо без нее
                        if keybord != None:
                            vk.messages.send(user_id=event.message.from_id, message=reply, random_id=0, keyboard=keybord)
                        else:
                            vk.messages.send(user_id=event.message.from_id, message=reply, random_id=0)   
                

                if event.type == VkBotEventType.WALL_POST_NEW and event.obj['from_id'] == -int(GROUPKZN_ID):
                    #id группы = event.object.owner_id
                    send_to_telegram(event=event) #пересылка поста в телеграм канал
                    users = subscriber.post_handler(event.object) #тянем из бд список подписчиков, чьи слова совпадают 
                
                    for user in users: #рассылаем пост
                        vk.messages.send(user_id=user, message="Новый пост!", attachment=f"wall-22156807_{event.object.id}", random_id=0)


        except Exception as e:
            # В случае ошибки, печатаем ее и продолжаем прослушивание
            print("разрыв соединения - казань")
            print(f"Error: {e}")
            time.sleep(5)  # Пауза перед попыткой подключения снова
     

if __name__ == '__main__':
    main()