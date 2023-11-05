from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from database.sql import get_tg_user_status, check_tg_user
from misc.config import OWNER_ID
import logging




class isOwner(BoundFilter):

    async def check(self, message: Message) -> bool:
        logging.debug(f"user {message.from_id}  in 'isExistCurrentGroup' filter")
        return True if message.from_id == OWNER_ID else False
    
class isUser(BoundFilter):

    async def check(self, message: Message) -> bool:
        logging.debug(f"user {message.from_id}  in 'isUser' filter")
        return True if check_tg_user(message.from_id) == 1 else False
    
