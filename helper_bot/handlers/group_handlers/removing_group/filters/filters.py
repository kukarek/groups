from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from database import sql 
from ...group_filters import *
        
     
class isRemovingGroup(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if sql.get_tg_user_status(message.from_id) == "removing group" else False