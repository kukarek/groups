import logging
from database import sql
from .keyboards import *
from .chat_logic import *
from .chat_logic import Response
from misc.config import ADMINS, API_TOKEN
from vk_api.bot_longpoll import VkBotMessageEvent
from vk_api.vk_api import VkApiMethod
from aiogram import Bot

#обработка входящего сообщения, возвращает текст ответа, клавиатуру, необходимость уведомить админа
def reply_message_handler(event: VkBotMessageEvent, vk_session):
    
    group_id = event.group_id
    user_id = event.message.from_id
    message_text = event.message.text


    handlers = {"0": none_status_handler,
                "start": start_status_handler,
                "employer": employer_status_handler,
                "employer_and_admin": employer_and_admin_status_handler,
                "applicant": applicant_status_handler,
                "editing": editing_status_handler}
    
    status = sql.get_status(user_id=user_id, group_id=group_id)[0]
    
    user_info = vk_session.get_api().users.get(user_ids=user_id)
    user_name = user_info[0]['first_name'] + " " + user_info[0]['last_name'] # Имя пользователя
    logging.debug(f"handling message '{message_text}' from '{user_name}' with status '{status}' ")

    response = handlers[status](user_id=user_id, message_text=message_text, group_id=group_id)

    return response

async def send_answer(vk: VkApiMethod, event: VkBotMessageEvent, response: Response, vk_session):
    
    user_info = vk_session.get_api().users.get(user_ids=event.message.from_id)
    user_name = user_info[0]['first_name'] + " " + user_info[0]['last_name'] # Имя пользователя



    if response.message != None: #отправка ответа юзеру с клавиатурой, либо без нее

        if response.keyboard != None:
            
            logging.debug(f"sending answer '{response.message}' with keyboard for '{user_name}' ")
            vk.messages.send(user_id=event.message.from_id, message=response.message, random_id=0, keyboard=response.keyboard)
        else:
            logging.debug(f"sending answer '{response.message}' without keyboard for '{user_name}' ")
            vk.messages.send(user_id=event.message.from_id, message=response.message, random_id=0) 

    #если это сообщение от админа
    if event.message.reply_message is not None:

        user_id = event.message.reply_message['text'].split("id")[1]

        vk.messages.send(user_id=user_id, message=event.message.text, random_id=0)
  
async def notife_admin(vk: VkApiMethod, event: VkBotMessageEvent, response: Response):
    
    if event.message.reply_message is None:
        if response.notify == True: 
            for admin in ADMINS:
                logging.debug(f"notifying admin '{admin}' with message '{event.message.text}' ")
                vk.messages.send(user_id=admin, message=f"Новое сообщение! от id{event.message.from_id}", forward_messages=event.message.id, random_id=0)
    
async def notife_BOB(event: VkBotMessageEvent, response: Response):
    
    if response.notify == True:
        bot = Bot(token=API_TOKEN["reposter"])
            
        if event.message.reply_message is not None:
            logging.debug(f"notifying 'BOB' in tg with message 'Ответил)' ")
            await bot.send_message(chat_id=6356732052, text="Ответил)")
        else:
            logging.debug(f"notifying 'BOB' in tg with message '{event.message.text}' ")
            await bot.send_message(chat_id=6356732052, text=f"Новое сообщение! '{event.message.text}'")


        await bot.close()