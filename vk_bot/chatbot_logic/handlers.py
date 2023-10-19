from database import sql
from misc.config import RULES_LINK, PAYMENT, EXAMPLE_WORDS
from .handlers import *
from .keyboards import *

class Response():
    
    keyboard = None
    message = None
    notify = None

    def __init__(self, message=None, keyboard=None, notify=None):
       
        self.message = message
        self.keyboard = keyboard
        self.notify = notify


#обработка сообщений, учитывая статус юзера, каждая функция должна возвращать текст ответа, клавиутуру, необходимость уведомить админа
def none_status_handler(user_id, message_text, group_id):
    
    if message_text == '/start' or message_text.lower() == 'start' or message_text == 'старт' or message_text.lower() == 'начать' or message_text.lower() == 'запустить':
         
        sql.add_user(user_id=user_id, group_id=group_id) #запись нового пользователя в бд, статус по умочланию = start

        return Response(message="Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?", 
                        keyboard=create_start_keyboard())
        
    else: 
        return Response(notify=True)

def start_status_handler(user_id, message_text, group_id):
    
    if message_text == 'Хочу разместить вакансию':
        
        sql.set_status(user_id=user_id, status="employer", group_id=group_id)
        
        return Response(message='Выберите действие на клавиатуре:', 
                        keyboard=create_employer_keyboard())

    elif message_text == 'Ищу работу':
        
        sql.set_status(user_id=user_id, status="applicant", group_id=group_id)
        keywords = sql.get_keywords(user_id=user_id, group_id=group_id)
        
        return Response(message='Выберите действие на клавиатуре:', 
                        keyboard=create_applicant_keyboard(keywords=keywords))

    else:
        return Response(message='Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', 
                        keyboard=create_start_keyboard())

def employer_status_handler(user_id, message_text, group_id):

    if message_text == "/start" or message_text == "Главное меню": #откат до статуса старт

        sql.set_status(user_id=user_id, status="start", group_id=group_id)

        return Response(message='Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', 
                        keyboard=create_start_keyboard())
    
    elif message_text == "Правила размещения":
        
        return Response(message=RULES_LINK)
    
    elif message_text == "Реквизиты":
        
        return Response(message=PAYMENT)

    elif message_text == "Позвать администратора":

        sql.set_status(user_id=user_id, status="employer_and_admin", group_id=group_id)

        return Response(message='Сейчас вам ответит администратор!', 
                        keyboard=create_employerandadmin_keyboard(), 
                        notify=True)        

    else:
        return Response(message='Выберите действие на клавиатуре:') 
    
def employer_and_admin_status_handler(user_id, message_text, group_id):

    if message_text == "/start" or message_text == "Главное меню": #откат до статуса старт

        sql.set_status(user_id=user_id, status="start", group_id=group_id)

        return Response(message='Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', 
                        keyboard=create_start_keyboard())
    
    elif message_text == "Правила размещения":

        return Response(message=RULES_LINK)
    
    elif message_text == "Реквизиты":

        return Response(message=PAYMENT)
    
    else:
        return Response(notify=True)

def editing_status_handler(user_id, message_text, group_id):
    
    if message_text == "/start" or message_text == "Главное меню":
        
        sql.remove_keywords(user_id=user_id, group_id=group_id)
        sql.set_status(user_id=user_id, status="start", group_id=group_id)
        return Response(message='Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', 
                        keyboard=create_start_keyboard())
    
    elif message_text == "": #если человек отправляет вложение без текста
        
        return Response(message='Отправьте текст с ключевыми словами через запятую!', 
                        keyboard=create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)))

    elif message_text == "Отменить подписку":

        sql.remove_keywords(user_id=user_id, group_id=group_id)
        sql.set_status(user_id=user_id, status="applicant", group_id=group_id)  

        return Response(message="Подписка отменена!", 
                        keyboard=create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)))
    
    elif message_text == "Редактировать ключевые слова" or message_text == "Добавить ключевые слова":
        
        return Response(message="Отправьте ключевые слова через запятую", 
                        keyboard=create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)))

    elif message_text == "Просмотреть ключевые слова":
        
        words = sql.get_keywords(user_id=user_id, group_id=group_id)
        if words:
            return Response(message=words[0])
        else:
            return Response(message="У вас нет ключевых слов для подписки :(", 
                            keyboard=create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)))

    elif message_text == "Пример слов":

        return Response(message=EXAMPLE_WORDS, 
                        keyboard=create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)))

    else:
        sql.set_keywords(user_id=user_id,keywords=message_text, group_id=group_id)
        sql.set_status(user_id=user_id, status="applicant", group_id=group_id)

        return Response(message="Подписка по вашим ключевым словам - активна!", 
                        keyboard=create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)))

def applicant_status_handler(user_id, message_text, group_id):
   
    if message_text == "/start" or message_text == "Главное меню": #откат до статуса старт
        
        sql.remove_keywords(user_id=user_id, group_id=group_id)
        sql.set_status(user_id=user_id, status="start", group_id=group_id) 

        return Response(message='Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', 
                        keyboard=create_start_keyboard())
    
    elif message_text == "Редактировать ключевые слова" or message_text == "Добавить ключевые слова":
        
        sql.set_status(user_id=user_id, status="editing", group_id=group_id)

        return Response(message="Отправьте ключевые слова через запятую", 
                        keyboard=create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)))

    elif message_text == "Просмотреть ключевые слова":
        
        words = sql.get_keywords(user_id=user_id, group_id=group_id)

        if words:
            return Response(message=words[0], 
                            keyboard=create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)))
        else:
            return Response(message="У вас нет ключевых слов для подписки :(", 
                            keyboard=create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)))

    elif message_text == "Пример слов":

        return Response(message="без опыта, официант, бармен, подработка, стройка, шабашка, оплата сразу", 
                        keyboard=create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)))

    elif message_text == "Отменить подписку":

        sql.remove_keywords(user_id=user_id, group_id=group_id)
        
        return Response(message="Подписка отменена!", 
                        keyboard=create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)))
    else:
        return Response(message='Выберите действие на клавиатуре:', 
                        keyboard=create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)))
