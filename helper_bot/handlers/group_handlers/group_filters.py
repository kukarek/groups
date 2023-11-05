import logging
from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from database import sql 
from ..main_filters import *

class isNoCurrentGroup(BoundFilter):

    async def check(self, message: Message):
        logging.debug(f"user {message.from_id}  in 'isNoCurrentGroup' filter")
        return True if sql.get_current_group_id(message.from_id) == "None" else False
    
class isExistCurrentGroup(BoundFilter):

    async def check(self, message: Message):
        logging.debug(f"user {message.from_id}  in 'isExistCurrentGroup' filter")
        return True if sql.get_current_group_id(message.from_id) != "None" else False
    
