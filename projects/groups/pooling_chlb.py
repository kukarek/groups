import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import asyncio
import aiogram
import time
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import subscriber


# Укажите токен VK бота и Telegram бота
VK_TOKEN = "vk1.a.jxR6pEkaRj7j9WNJ1DBtNvolxfLtUCAZvzxSb3-WJrLUnRemjz85aI86IAUPZEiYrjRTCoUDhLYv56F41eashHp6Dq-onnhDotpXBDrlyELDI3h_qIwu4iUKvTjuC1GSSZ_MWvHZrIl32fRIKGWLZYxBvCMF5BJqaQ9uBg6KsJfaarJBV1jx9ym6aOn2us8wBZundpknFnq3kAafJk4Fog"
TELEGRAM_TOKEN = "6470735932:AAHG7LzA_VtGZvmK5JopIMqoiNa3CmuEvuM"
CHANNEL_ID = "-1001948046451"  # Замените на свой канал
TELEGRAM_CHAT_ID = "1020541698"


def connect_vk():
   # Инициализация VK бота
   vk_session = vk_api.VkApi(token=VK_TOKEN)
   longpoll = VkBotLongPoll(vk_session, "220670949")  # Замените на ваш ID группы
   return longpoll

# Инициализация Telegram бота
async def send_telegram(image, caption):
    
    bot = Bot(token=TELEGRAM_TOKEN)
    
    if image=="":
      
      try:

          await bot.send_message(chat_id=CHANNEL_ID, text=caption)

      except aiogram.utils.exceptions.BadRequest as e:
      
          print(f"Error sending text(челябинск): {e}")
       
      
    else:
      
      try:

          await bot.send_photo(chat_id=CHANNEL_ID, photo=image, caption=caption)

      except aiogram.utils.exceptions.BadRequest as e:
      
          print(f"Error sending media group(челябинск): {e}")

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
        longpoll = VkBotLongPoll(vk_session, "220670949")  # Замените на ваш ID группы
        vk = vk_session.get_api()
        
        print("соединение установлено - челябинск")
        try:
           # Отслеживание новых записей на стене VK
           for event in longpoll.listen():
              
             if event.type == VkBotEventType.MESSAGE_NEW:
                #id группы = event.group_id
                reply, keybord, notify = subscriber.reply_message_handler(event=event)

                if notify == True: #уведомление админа
                   vk.messages.send(user_id=732405775, message=f"Новое сообщение! '{event.message.text}'", random_id=0)

                if reply != None: #отправка ответа юзеру с клавиатурой, либо без нее
                   if keybord != None:
                      vk.messages.send(user_id=event.message.from_id, message=reply, random_id=0, keyboard=keybord)
                   else:
                      vk.messages.send(user_id=event.message.from_id, message=reply, random_id=0) 
                
             if event.type == VkBotEventType.WALL_POST_NEW:
                #id группы = event.object.owner_id
                send_to_telegram(event=event) #пересылка поста в телеграм канал
                users = subscriber.post_handler(event.object) #тянем из бд список подписчиков, чьи слова совпадают 
                
                for user in users: #рассылаем пост
                   vk.messages.send(user_id=user, message="Новый пост!", attachment=f"wall-220670949_{event.object.id}", random_id=0)

        except Exception as e:
            # В случае ошибки, печатаем ее и продолжаем прослушивание
            print("разрыв соединения - челябинск")
            print(f"Error: {e}")
            time.sleep(1)  # Пауза перед попыткой подключения снова
     

if __name__ == '__main__':
    main()