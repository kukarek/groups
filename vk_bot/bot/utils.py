import aiogram
from aiogram import Bot 
from misc.config import API_TOKEN, CHANNEL_ID, ADMINS
from database import sql


async def send_to_telegram(event):
    """
    Send vk post to telegram channel

    """
    bot = Bot(token=API_TOKEN["reposter"])

    message = event.object.text

    if len(message) in range(0, 1000) and event.object.attachments and "photo" in event.object.attachments[0]:

        photo_url = event.object.attachments[0]["photo"]["sizes"][-1]["url"]
        await bot.send_photo(chat_id=CHANNEL_ID, photo=photo_url, caption=message)
      

    elif len(message) in range(0, 4000):

        await bot.send_message(chat_id=CHANNEL_ID, text=message)

    await bot.close()

async def sending_post_to_users(vk, event):
    
    post = event.object

    users = sql.get_users_data_as_dict(group_id=post.owner_id)
    
    matching_users = []

    for user in users:
        
        user_id = user['user_id']
        keywords = user['keywords']

        keyword_list = keywords.split(',')

        for keyword in keyword_list:
            if keyword in post.text.lower():
                matching_users.append(user_id)
                break  # Для оптимизации - если слово найдено, выходим из внутреннего цикла

    for user in users: #рассылаем пост
        await vk.messages.send(user_id=user, message="Новый пост!", attachment=f"wall-22156807_{event.object.id}", random_id=0)

async def send_answer(vk, event, response):
        
    if response.message != None: #отправка ответа юзеру с клавиатурой, либо без нее

        if response.keyboard != None:
            
            vk.messages.send(user_id=event.message.from_id, message=response.message, random_id=0, keyboard=response.keyboard)
        else:
            vk.messages.send(user_id=event.message.from_id, message=response.message, random_id=0) 

async def notife_admin(vk, event, response):
    
    if response.notify == True: 
        for admin in ADMINS:
            vk.messages.send(user_id=admin, message=f"Новое сообщение! '{event.message.text}'", random_id=0)
