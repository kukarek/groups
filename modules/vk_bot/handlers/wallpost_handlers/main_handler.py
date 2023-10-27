import logging
from aiogram import Bot 
from misc.config import API_TOKEN, CHANNEL_ID
from database import sql


async def send_to_telegram(event):
    """
    Send vk post to telegram channel

    """
    bot = Bot(token=API_TOKEN["reposter"])

    message = event.object.text

    if len(message) in range(0, 1000) and event.object.attachments and "photo" in event.object.attachments[0]:

        photo_url = event.object.attachments[0]["photo"]["sizes"][-1]["url"]
        logging.debug("sending post with photo to telegram")
        await bot.send_photo(chat_id=CHANNEL_ID, photo=photo_url, caption=message)
      

    elif len(message) in range(0, 4000):

        logging.debug("sending post without photo to telegram")
        await bot.send_message(chat_id=CHANNEL_ID, text=message)

    await bot.close()

async def sending_post_to_users(vk, event):
    
    post = event.object

    users = sql.get_users_data_as_dict(group_id=post.owner_id)
    
    matching_users = []

    logging.debug("finding users with matching keywords")
    for user in users:
        
        user_id = user['user_id']
        keywords = user['keywords']

        keyword_list = keywords.split(',')

        for keyword in keyword_list:
            if keyword in post.text.lower():
                matching_users.append(user_id)
                break  # Для оптимизации - если слово найдено, выходим из внутреннего цикла
    
    if matching_users:
        logging.debug(f"sending wallpost to users ({len(matching_users)}) with matching keywords")
        for user in users: #рассылаем пост
            logging.debug(f"sending wallpost to user {user}")
            vk.messages.send(user_id=user["user_id"], message="Новый пост!", attachment=f"wall-22156807_{event.object.id}", random_id=0)

