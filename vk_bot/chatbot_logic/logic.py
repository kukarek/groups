from database import sql
from vk_api.keyboard import VkKeyboard
from .keyboards import *
from .handlers import *

#обработка входящего сообщения, возвращает текст ответа, клавиатуру, необходимость уведомить админа
def reply_message_handler(event):
    
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

    response = handlers[status](user_id=user_id, message_text=message_text, group_id=group_id)
        
    return response



