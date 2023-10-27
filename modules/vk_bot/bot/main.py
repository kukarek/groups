import vk_api 
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import asyncio
import time
from misc.config import GROUPKZN_ID, API_TOKEN
from .events_handler import *
from database import sql
import logging
from log.loggHandler import ERROR

logg = logging.getLogger(__name__)
vk_session = vk_api.VkApi(token=API_TOKEN['vk'])
longpoll = VkBotLongPoll(vk_session, GROUPKZN_ID)
vk = vk_session.get_api()

def init():
    logg.addHandler(ERROR(vk=vk))
    sql.create_connection()


def start_bot():

    init() 

    logg.info("SUCCESS CONNECTION (vk_bot)")

    try:
        for event in longpoll.listen():
            
            if event.type == VkBotEventType.MESSAGE_NEW:
                asyncio.run(message_handler(vk, event, vk_session))

            if event.type == VkBotEventType.WALL_POST_NEW and event.obj['from_id'] == -int(GROUPKZN_ID):
                asyncio.run(wallpost_handler(vk, event))
                
    except Exception as e:
        # В случае ошибки, печатаем ее и продолжаем прослушивание
        logg.error(e)
        # Пауза перед попыткой переподключения
        time.sleep(5)  


if __name__ == '__main__':
    start_bot()