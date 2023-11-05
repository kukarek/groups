from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from database.sql import get_tg_user_status
from ...main_filters import *
import logging

class isAddingGroupName(BoundFilter):

    async def check(self, message: types.Message) -> bool:
        logging.debug(f"user {message.from_id}  in 'isAddingGroupName' filter")
        return True if get_tg_user_status(message.from_id) == "adding group name" else False
    
class isAddingGroupID(BoundFilter):

    async def check(self, message: types.Message) -> bool:
        logging.debug(f"user {message.from_id}  in 'isAddingGroupID' filter")
        return True if get_tg_user_status(message.from_id) == "adding group id" else False

class isAddingVkToken(BoundFilter):

    async def check(self, message: types.Message) -> bool:
        logging.debug(f"user {message.from_id}  in 'isAddingVkToken' filter")
        return True if get_tg_user_status(message.from_id) == "adding vk token" else False
    
class isAddingVkWallToken(BoundFilter):

    async def check(self, message: types.Message) -> bool:
        logging.debug(f"user {message.from_id}  in 'isAddingVkWallToken' filter")
        return True if get_tg_user_status(message.from_id) == "adding vk wall token" else False
    
class isAddingVkAdmin(BoundFilter):

    async def check(self, message: types.Message) -> bool:
        logging.debug(f"user {message.from_id}  in 'isAddingVkAdmin' filter")
        return True if get_tg_user_status(message.from_id) == "adding vk admin" else False