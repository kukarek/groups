import vk_api 
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import asyncio
import time
from .events_handler import EventHandler
import logging
from log.loggHandler import ERROR
from logging import Logger

class Bot(EventHandler):

    logg: Logger = None
    
    VK_TOKEN = None
    GROUP_ID = None
    GROUP_NAME = None

    isActiveBot = False

    def init(self):
        
        self.vk_session = vk_api.VkApi(token=self.VK_TOKEN)
        self.longpoll = VkBotLongPoll(self.vk_session, self.GROUP_ID)
        self.vk = self.vk_session.get_api()

        self.logg = logging.getLogger(self.GROUP_NAME)
        self.logg.addHandler(ERROR(vk=self.vk, group_id=self.GROUP_ID))

    def start_bot(self):

        self.init() 

        self.logg.info(f"SUCCESS CONNECTION BOT {self.GROUP_NAME}")

        try:
    
            for event in self.longpoll.listen():
                
                if self.isActiveBot == False:
                    self.logg.info(f"STOPPING BOT {self.GROUP_NAME}")
                    return

                if event.type == VkBotEventType.MESSAGE_NEW:
                    asyncio.run(self.message_handler(self.vk, event, self.vk_session))

                if event.type == VkBotEventType.WALL_POST_NEW and event.obj['from_id'] == -int(self.GROUP_ID):
                    asyncio.run(self.wallpost_handler(self.vk, event))
                
        except Exception as e:
            # В случае ошибки, печатаем ее и продолжаем прослушивание
            self.logg.info(e)
            # Пауза перед попыткой переподключения
            time.sleep(5)  
            self.start_bot()

        