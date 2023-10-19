from ..chatbot_logic.logic import reply_message_handler
from .utils import *

async def message_handler(vk, event):
                
    response = reply_message_handler(event=event)

    await send_answer(response=response, vk=vk, event=event)
    await notife_admin(response=response, vk=vk, event=event)

async def wallpost_handler(vk, event):
    
    #пересылка поста в телеграм канал
    await send_to_telegram(event) 
    #рассылка поста подписчикам
    await sending_post_to_users(vk, event)
    