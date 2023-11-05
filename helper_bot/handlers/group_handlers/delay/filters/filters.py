from aiogram.dispatcher.filters import BoundFilter
from database import sql 
from aiogram.types import Message
from ...group_filters import *
import logging

class IsSettingDate(BoundFilter):

    async def check(self, message: Message) -> bool:
        logging.debug(f"user {message.from_id}  in 'IsSettingDate' filter")
        return True if sql.get_tg_user_status(message.from_id) == "setting date" else False
    
class IsSettingStartHour(BoundFilter):

    async def check(self, message: Message) -> bool:
        logging.debug(f"user {message.from_id}  in 'IsSettingStartHour' filter")
        return True if sql.get_tg_user_status(message.from_id) == "setting start hour" else False
    
class IsSettingEndHour(BoundFilter):

    async def check(self, message: Message) -> bool:
        logging.debug(f"user {message.from_id}  in 'IsSettingEndHour' filter")
        return True if sql.get_tg_user_status(message.from_id) == "setting end hour" else False
    
class IsRemovingParser(BoundFilter):

    async def check(self, message: Message) -> bool:
        logging.debug(f"user {message.from_id}  in 'IsRemovingParser' filter")
        return True if sql.get_tg_user_status(message.from_id) == "removing parser" else False
    
class IsAdditingParser(BoundFilter):

    async def check(self, message: Message) -> bool:
        logging.debug(f"user {message.from_id}  in 'IsAdditingParser' filter")
        return True if sql.get_tg_user_status(message.from_id) == "additing parser" else False
    
class isEditingDefaultPhoto(BoundFilter):

    async def check(self, message: Message):
        logging.debug(f"user {message.from_id}  in 'isEditingDefaultPhoto' filter")
        return True if sql.get_tg_user_status(message.from_id) == "editing default photo" else False