from aiogram.dispatcher.filters import BoundFilter
from aiogram import types


mini_db = {
    1020541698: None
}


        
class isSettingCycle(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if mini_db[message.from_id] == "setting cycle" else False
     
class isSettingTimer(BoundFilter):

    async def check(self, message: types.Message) -> bool:

        return True if mini_db[message.from_id] == "setting timer" else False