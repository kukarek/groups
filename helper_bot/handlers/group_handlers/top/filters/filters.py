from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from database import sql 
from ...group_filters import *

    
class isAddingTopKeywords(BoundFilter):

    async def check(self, message: Message):
        logging.debug(f"user {message.from_id}  in 'isAddingTopKeywords' filter")
        return True if sql.get_tg_user_status(message.from_id) == "adding top keywords" else False


