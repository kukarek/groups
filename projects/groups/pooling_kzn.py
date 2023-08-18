import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import asyncio
import aiogram
import time
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


# Укажите токен VK бота и Telegram бота
VK_TOKEN = "vk1.a.wYlKxh7CuxPS0UHp3F8SRLatcPewyEHqerQJrtrBOc077tEdHTIkBq5EbUeGPvMef02_kB6I2IaSMEf9CjTgH_hpdjSfdn6pAq1aX0J1WBbUKONpxrMgPLW0UzMfrKwz0a2mxoUJ5AgXcZXF-crp67TFpib-WIJRk6asj2lmevOjBgin05SOJdX7x346Q8nOkImWqkRCJFGJv5d1sabGzw"
TELEGRAM_TOKEN = "6589082148:AAGlKY-mhuDxHtPMmJayoVXRpPnSMBRswhU"
CHANNEL_ID = "-1001962325633"  # Замените на свой канал


def connect_vk():
   # Инициализация VK бота
   vk_session = vk_api.VkApi(token=VK_TOKEN)
   longpoll = VkBotLongPoll(vk_session, "22156807")  # Замените на ваш ID группы
   return longpoll



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




def main():
    
    

    while True:
        
        vk_session = vk_api.VkApi(token=VK_TOKEN)
        longpoll = VkBotLongPoll(vk_session, "22156807")  # Замените на ваш ID группы
        vk = vk_session.get_api()
        

        print("соединение установлено- казань")
        try:
           
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
            print("разрыв соединения - казань")
            print(f"Error: {e}")
            time.sleep(1)  # Пауза перед попыткой подключения снова
     

if __name__ == '__main__':
    main()