from logging import Logger
from database import sql
from .chat_logic import ChatLogic
from .chat_logic import Response
from vk_api.bot_longpoll import VkBotMessageEvent
from vk_api.vk_api import VkApiMethod


class MessageHandler(ChatLogic):

    logg: Logger = None

    def ADMINS(self, group_id):

        admins = sql.get_vk_admins(group_id)
        return admins

    #обработка входящего сообщения, возвращает текст ответа, клавиатуру, необходимость уведомить админа
    def reply_message_handler(self, event: VkBotMessageEvent, vk_session):
        
        group_id = event.group_id
        user_id = event.message.from_id
        message_text = event.message.text


        handlers = {"0": self.none_status_handler,
                    "start": self.start_status_handler,
                    "employer": self.employer_status_handler,
                    "employer_and_admin": self.employer_and_admin_status_handler,
                    "applicant": self.applicant_status_handler,
                    "editing": self.editing_status_handler}
        
        status = sql.get_status(user_id=user_id, group_id=group_id)[0]
        
        user_info = vk_session.get_api().users.get(user_ids=user_id)
        user_name = user_info[0]['first_name'] + " " + user_info[0]['last_name'] # Имя пользователя
        self.logg.debug(f"handling message '{message_text}' from '{user_name}' with status '{status}' ")

        response = handlers[status](user_id=user_id, message_text=message_text, group_id=group_id)

        return response

    async def send_answer(self, vk: VkApiMethod, event: VkBotMessageEvent, response: Response, vk_session):
        
        user_info = vk_session.get_api().users.get(user_ids=event.message.from_id)
        user_name = user_info[0]['first_name'] + " " + user_info[0]['last_name'] # Имя пользователя

        if response.message != None: #отправка ответа юзеру с клавиатурой, либо без нее

            if response.keyboard != None:
                
                self.logg.debug(f"sending answer '{response.message}' with keyboard for '{user_name}' ")
                vk.messages.send(user_id=event.message.from_id, message=response.message, random_id=0, keyboard=response.keyboard)
            else:
                self.logg.debug(f"sending answer '{response.message}' without keyboard for '{user_name}' ")
                vk.messages.send(user_id=event.message.from_id, message=response.message, random_id=0) 

        #если это сообщение от админа
        if event.message.reply_message is not None:

            user_id = event.message.reply_message['text'].split("id")[1]

            vk.messages.send(user_id=user_id, message=event.message.text, random_id=0)
    
    async def notife_admin(self, vk: VkApiMethod, event: VkBotMessageEvent, response: Response):
        
        if event.message.reply_message is None and response.notify:
        
            try:
                if self.ADMINS(event.group_id):
                    for admin in self.ADMINS(event.group_id):
                        self.logg.debug(f"notifying admin '{admin}' with message '{event.message.text}' ")
                        vk.messages.send(user_id=admin, message=f"Новое сообщение! от id{event.message.from_id}", forward_messages=event.message.id, random_id=0)
            except Exception as e:
                self.logg.critical(e)