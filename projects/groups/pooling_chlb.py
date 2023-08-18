import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import asyncio
import aiogram
import time
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


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
                content = event.message.text
                vk.messages.send(user_id=732405775, message=f"Новое сообщение! '{content}'", random_id=0)
                
             if event.type == VkBotEventType.WALL_POST_NEW:
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

        except Exception as e:
            # В случае ошибки, печатаем ее и продолжаем прослушивание
            print("разрыв соединения - челябинск")
            print(f"Error: {e}")
            time.sleep(1)  # Пауза перед попыткой подключения снова
     

if __name__ == '__main__':
    main()