from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from database import sql 
from ...group_filters import *

    
class isAddingVkAdmin(BoundFilter):

    async def check(self, message: Message):
        logging.debug(f"user {message.from_id}  in 'isAddingVkAdmin' filter")
        return True if sql.get_tg_user_status(message.from_id) == "adding vk admin" else False

class isRemovingVkAdmin(BoundFilter):

    async def check(self, message: Message):
        logging.debug(f"user {message.from_id}  in 'isRemovingVkAdmin' filter")
        return True if sql.get_tg_user_status(message.from_id) == "removing vk admin" else False

class isEditingRulesLink(BoundFilter):

    async def check(self, message: Message):
        logging.debug(f"user {message.from_id}  in 'isEditingRulesLink' filter")
        return True if sql.get_tg_user_status(message.from_id) == "editing rules link" else False

class isEditingExampleWords(BoundFilter):

    async def check(self, message: Message):
        logging.debug(f"user {message.from_id}  in 'isEditingExampleWords' filter")
        return True if sql.get_tg_user_status(message.from_id) == "editing example words" else False

class isEditingPayment(BoundFilter):

    async def check(self, message: Message):
        logging.debug(f"user {message.from_id}  in 'isEditingPayment' filter")
        return True if sql.get_tg_user_status(message.from_id) == "editing payment" else False

class isEditingSearchWords(BoundFilter):

    async def check(self, message: Message):
        logging.debug(f"user {message.from_id}  in 'isEditingSearchWords' filter")
        return True if sql.get_tg_user_status(message.from_id) == "editing search words" else False

