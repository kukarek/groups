from .bot import Bot
from .modules import Modules
from database import sql  
import threading
import logging 
import aiogram
import asyncio
from misc import config

class Group(Bot, Modules):

    logg = logging.getLogger()
    #поток для vk_longpoll
    vk_bot = None

    def __init__(self, group_id) -> None:
        
        data = sql.get_group_data(group_id)
        
        self.GROUP_ID = group_id
        self.OWNER_ID = data["OWNER_ID"]
        self.GROUP_NAME = data["GROUP_NAME"]
        self.VK_TOKEN = data["VK_TOKEN"]
        self.VK_TOKEN_FOR_DELAY = data["VK_TOKEN_FOR_DELAY"]

        if data["example_words"]:
            self.EXAMPLE_WORDS = data["example_words"]
        if data["rules_link"]:
            self.RULES_LINK = data["rules_link"]
        if data["payment"]:
            self.PAYMENT = data["payment"]

        sql.create_group_users_table(self.GROUP_ID)

    def start(self):
        
        try:
            if self.isActiveBot:
                return
            else:
                #вк лонгпул считывает метку isActiveBot только после возникновения события
                #если событий еще не было, и поток активен, просто меняем метку на True
                if self.vk_bot and self.vk_bot.is_alive():
                    self.isActiveBot = True
                else:
                    self.isActiveBot = True
                    self.vk_bot = threading.Thread(target=self.start_bot)
                    self.vk_bot.start()
            
        except Exception as e:
            self.logg.critical(e)

    def stop_chat_bot(self):
        self.isActiveBot = False
       




    