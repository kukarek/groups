from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sql

class Response:

    print()

# Создаем клавиатуры
def create_start_keyboard():
    
    keyboard_start = VkKeyboard(one_time=True)

    # Добавляем кнопки
    keyboard_start.add_button('Хочу разместить вакансию', color=VkKeyboardColor.POSITIVE)
    keyboard_start.add_button('Ищу работу', color=VkKeyboardColor.POSITIVE)

    return keyboard_start.get_keyboard()

def create_employerandadmin_keyboard():

    keyboard = VkKeyboard()

    keyboard.add_button('Правила размещения', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Реквизиты', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Главное меню', color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()

def create_employer_keyboard():
    
    keyboard_employer = VkKeyboard()

    # Добавляем кнопки
    keyboard_employer.add_button('Позвать администратора', color=VkKeyboardColor.POSITIVE)
    keyboard_employer.add_line()
    keyboard_employer.add_button('Правила размещения', color=VkKeyboardColor.POSITIVE)
    keyboard_employer.add_line()
    keyboard_employer.add_button('Реквизиты', color=VkKeyboardColor.POSITIVE)
    keyboard_employer.add_line()
    keyboard_employer.add_button('Главное меню', color=VkKeyboardColor.POSITIVE)

    return keyboard_employer.get_keyboard()

def create_applicant_keyboard(keywords):
    
    keyboard_applicant = VkKeyboard(one_time=True)
    
    if keywords:
        button_text = 'Редактировать ключевые слова'
    else:
        button_text = 'Добавить ключевые слова'

    # Добавляем кнопки
    keyboard_applicant.add_button(f'{button_text}', color=VkKeyboardColor.POSITIVE)
    keyboard_applicant.add_line()
    if keywords:
        keyboard_applicant.add_button('Просмотреть ключевые слова', color=VkKeyboardColor.POSITIVE)
        keyboard_applicant.add_line()
    keyboard_applicant.add_button('Пример слов', color=VkKeyboardColor.POSITIVE)
    keyboard_applicant.add_line()
    keyboard_applicant.add_button('Главное меню', color=VkKeyboardColor.POSITIVE)
    if keywords:
        keyboard_applicant.add_line()
        keyboard_applicant.add_button('Отменить подписку', color=VkKeyboardColor.NEGATIVE)

    return keyboard_applicant.get_keyboard()

#обработка сообщений, учитывая статус юзера, каждая функция должна возвращать текст ответа, клавиутуру, необходимость уведомить админа
def none_status_handler(user_id, message_text, group_id):
    
    if message_text == '/start' or message_text.lower() == 'start' or message_text == 'старт' or message_text.lower() == 'начать' or message_text.lower() == 'запустить':
         
        sql.add_user(user_id=user_id, group_id=group_id) #запись нового пользователя в бд, статус по умочланию = start
        return 'Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', create_start_keyboard(), None
        
    else: 
        return None, None, True #бот не обрабатывает сообщение, уведомляет админа

def start_status_handler(user_id, message_text, group_id):
    
    if message_text == 'Хочу разместить вакансию':
        
        sql.set_status(user_id=user_id, status="employer", group_id=group_id)
        
        return 'Выберите действие на клавиатуре:', create_employer_keyboard(), None

    elif message_text == 'Ищу работу':
        
        sql.set_status(user_id=user_id, status="applicant", group_id=group_id)
        keywords = sql.get_keywords(user_id=user_id, group_id=group_id)
        
        return 'Выберите действие на клавиатуре:', create_applicant_keyboard(keywords=keywords), None

    else:
        return 'Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', create_start_keyboard(), None

def employer_status_handler(user_id, message_text, group_id):

    if message_text == "/start" or message_text == "Главное меню": #откат до статуса старт

        sql.set_status(user_id=user_id, status="start", group_id=group_id)

        return 'Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', create_start_keyboard(), None
    
    elif message_text == "Правила размещения":
        
        if group_id == 22156807:
            link = "https://vk.com//@rabotakazank-vakans"
        if group_id == 220670949:
            link = "https://vk.com//@rabotachelyabynsk-vakans"

        return link, None, None
    
    elif message_text == "Реквизиты":
        
        text = '+7(986)913-68-24\nДмитрий(сбер/тинькофф)\n\nЛибо по СБП\nhttps://qr.nspk.ru/BS1A007PS0I8FECQ8EHRG2776H572NUP?type=01&bank=100000000004&crc=5453'

        return text, None, None

    elif message_text == "Позвать администратора":

        sql.set_status(user_id=user_id, status="employer_and_admin", group_id=group_id)

        return 'Сейчас вам ответит администратор!', create_employerandadmin_keyboard, True        

    else:
        return 'Выберите действие на клавиатуре:', None, None 
    
def employer_and_admin_status_handler(user_id, message_text, group_id):

    if message_text == "/start" or message_text == "Главное меню": #откат до статуса старт

        sql.set_status(user_id=user_id, status="start", group_id=group_id)

        return 'Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', create_start_keyboard(), None
    
    elif message_text == "Правила размещения":
        
        if group_id == 22156807:
            link = "https://vk.com//@rabotakazank-vakans"
        if group_id == 220670949:
            link = "https://vk.com//@rabotachelyabynsk-vakans"

        return link, None, None
    
    elif message_text == "Реквизиты":
        
        text = '+7(986)913-68-24\nДмитрий(сбер/тинькофф)\n\nЛибо по СБП\nhttps://qr.nspk.ru/BS1A007PS0I8FECQ8EHRG2776H572NUP?type=01&bank=100000000004&crc=5453'

        return text, None, None
    
    else:
        return None, None, True #бот не обрабатывает сообщение, переписка с админом 

def editing_status_handler(user_id, message_text, group_id):
    
    if message_text == "/start" or message_text == "Главное меню":
        
        sql.remove_keywords(user_id=user_id, group_id=group_id)
        sql.set_status(user_id=user_id, status="start", group_id=group_id)
        return 'Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', create_start_keyboard(), None
    
    elif message_text == "": #если человек отправляет вложение без текста
        
        return 'Отправьте текст с ключевыми словами через запятую!', create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)), None

    elif message_text == "Отменить подписку":

        sql.remove_keywords(user_id=user_id, group_id=group_id)
        sql.set_status(user_id=user_id, status="applicant", group_id=group_id)  
        return "Подписка отменена!", create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)), None
    
    elif message_text == "Редактировать ключевые слова" or message_text == "Добавить ключевые слова":
        
        return "Отправьте ключевые слова через запятую", create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)), None

    elif message_text == "Просмотреть ключевые слова":
        
        words = sql.get_keywords(user_id=user_id, group_id=group_id)
        if words:
            return words[0], None, None
        else:
            return "У вас нет ключевых слов для подписки :(", create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)), None

    elif message_text == "Пример слов":
        return "без опыта, официант, бармен, подработка, стройка, шабашка, оплата сразу", create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)), None

    else:
        
        sql.set_keywords(user_id=user_id,keywords=message_text, group_id=group_id)
        sql.set_status(user_id=user_id, status="applicant", group_id=group_id)   
        return "Подписка по вашим ключевым словам - активна!", create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)), None

def applicant_status_handler(user_id, message_text, group_id):
   
    if message_text == "/start" or message_text == "Главное меню": #откат до статуса старт
        
        sql.remove_keywords(user_id=user_id, group_id=group_id)
        sql.set_status(user_id=user_id, status="start", group_id=group_id) 
        return 'Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', create_start_keyboard(), None
    
    elif message_text == "Редактировать ключевые слова" or message_text == "Добавить ключевые слова":
        
        sql.set_status(user_id=user_id, status="editing", group_id=group_id)

        return "Отправьте ключевые слова через запятую", create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)), None

    elif message_text == "Просмотреть ключевые слова":
        
        words = sql.get_keywords(user_id=user_id, group_id=group_id)
        if words:
            return words[0], create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)), None
        else:
            return "У вас нет ключевых слов для подписки :(", create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)), None

    elif message_text == "Пример слов":
        return "без опыта, официант, бармен, подработка, стройка, шабашка, оплата сразу", create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)), None

    elif message_text == "Отменить подписку":

        sql.remove_keywords(user_id=user_id, group_id=group_id)
        return "Подписка отменена!", create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)), None

    else:
        return 'Выберите действие на клавиатуре:', create_applicant_keyboard(keywords=sql.get_keywords(user_id=user_id, group_id=group_id)), None

#функция поиска соответствий в тексте
def find_matching_users(users_data, post_text):
    matching_users = []

    for user in users_data:
        user_id = user['user_id']
        keywords = user['keywords']

        # Разделение ключевых слов на отдельные слова
        keyword_list = keywords.split(',')

        for keyword in keyword_list:
            if keyword in post_text.lower():
                matching_users.append(user_id)
                break  # Для оптимизации - если слово найдено, выходим из внутреннего цикла

    return matching_users
       
#обработка поста, возвращает id юзеров для рассылки поста
def post_handler(post): 

    group_id = post.owner_id

    users_data = sql.get_users_data_as_dict(group_id=group_id) #получаем данные из бд в словарь
    
    matching_users = find_matching_users(users_data=users_data, post_text=post.text) #функция поиска соответствий

    return matching_users

#обработка входящего сообщения, возвращает текст ответа, клавиатуру, необходимость уведомить админа
def reply_message_handler(event):
    
    group_id = event.group_id
    user_id = event.message.from_id
    message_text = event.message.text
                                    
    status = sql.get_status(user_id=user_id, group_id=group_id)[0]
        
    if status == "start":
        response, keybord, notify = start_status_handler(user_id=user_id,message_text=message_text, group_id=group_id)

    elif status == "employer":
        response, keybord, notify = employer_status_handler(user_id=user_id,message_text=message_text, group_id=group_id)

    elif status == "employer_and_admin":
        response, keybord, notify = employer_and_admin_status_handler(user_id=user_id,message_text=message_text, group_id=group_id)

    elif status == "applicant":
        response, keybord, notify = applicant_status_handler(user_id=user_id,message_text=message_text, group_id=group_id)

    elif status == "editing":
        response, keybord, notify = editing_status_handler(user_id=user_id,message_text=message_text, group_id=group_id)

    else:
        response, keybord, notify = none_status_handler(user_id=user_id,message_text=message_text, group_id=group_id)
        
    return response, keybord, notify



