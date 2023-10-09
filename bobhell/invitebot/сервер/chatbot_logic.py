import sql

#обработка первого сообщения, юзера нет в бд
def start_status_handler(user_id, message_text):
    
    if message_text == '/start':
         
        sql.add_user(user_id=user_id) #запись нового пользователя в бд, начальный статус = phone
        text = ("Приветствую, чтобы работать в тиме, вам нужно оставить заявку\n"+
               "Мы постараемся ее обработать как можно скорее\n\n"+
               "1. Модель телефона?")

        return text, None
        

def phone_answer_handler(user_id, message_text):
    
    sql.set_phone(user_id=user_id, phone=message_text)
    sql.set_status(user_id=user_id, status="time")
  
    response = "2. Сколько времени готовы уделять?"

    return response, None

def time_answer_handler(user_id, message_text):
    
    sql.set_time(user_id=user_id, time=message_text)
    sql.set_status(user_id=user_id, status="exp")
  
    response = "3. Ваш опыт работы (распишите подробно)"

    return response, None

def exp_answer_handler(user_id, message_text):
    
    sql.set_exp(user_id=user_id, exp=message_text)
    sql.set_status(user_id=user_id, status="lolz")
  
    response = "4. Ваш лолз"

    return response, None

def lolz_answer_handler(user_id, message_text):
    
    sql.set_lolz(user_id=user_id, lolz=message_text)
    sql.set_status(user_id=user_id, status="check")
  
    info = sql.get_user_info(user_id=user_id) 

    notify = info_handler(info)

    response = "Ваша заявка отправлена на рассмотрение, ожидайте решение администрации!"

    return response, notify

def info_handler(info):

    notify_str = ""

    notify_str = ("Новая заявка!\n\n"+
                  f"Модель телефона: {info[2]} \n\n"+
                  f"График: {info[3]}\n\n"+
                  f"Опыт работы: {info[4]}\n\n"+
                  f"Лолз: {info[5]}\n\n")

    return notify_str


    
#обработка входящего сообщения, возвращает текст ответа, клавиатуру, необходимость уведомить админа
def reply_message_handler(user_id, message_text):
                                        
    status = sql.get_status(user_id=user_id)[0]
        
    if status == "0":
        response, notify = start_status_handler(user_id=user_id,message_text=message_text)

    elif status == "phone":
        response, notify = phone_answer_handler(user_id=user_id,message_text=message_text)

    elif status == "time":
        response, notify = time_answer_handler(user_id=user_id,message_text=message_text)

    elif status == "exp":
        response, notify = exp_answer_handler(user_id=user_id,message_text=message_text)

    elif status == "lolz":
        response, notify = lolz_answer_handler(user_id=user_id,message_text=message_text)
    
    elif status == "check":
        response, notify = None, None

    return response, notify



