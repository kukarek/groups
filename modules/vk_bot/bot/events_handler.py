from ..handlers.message_handlers.main_handler import *
from ..handlers.wallpost_handlers.main_handler import *
import logging
from log.loggHandler import ERROR

logg = logging.getLogger(__name__)


async def message_handler(vk, event, vk_session):
    
    logg.addHandler(ERROR(vk=vk))

    try:
        response = reply_message_handler(event=event, vk_session=vk_session)

        await send_answer(response=response, vk=vk, event=event, vk_session=vk_session)
        await notife_admin(response=response, vk=vk, event=event)
        await notife_BOB(response=response, event=event)
    except Exception as e:
        logg.error(e)

async def wallpost_handler(vk, event):
    
    logg.addHandler(ERROR(vk=vk))

    try:
        #пересылка поста в телеграм канал
        await send_to_telegram(event) 
        #рассылка поста подписчикам
        await sending_post_to_users(vk, event)
    except Exception as e:
        logg.error(e)
    