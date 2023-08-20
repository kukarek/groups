import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlite3
import random

# Создаем клавиатуры
def create_start_keyboard():
    
    keyboard_start = VkKeyboard(one_time=True)

    # Добавляем кнопки
    keyboard_start.add_button('Хочу разместить вакансию', color=VkKeyboardColor.POSITIVE)
    keyboard_start.add_button('Ищу работу', color=VkKeyboardColor.POSITIVE)

    return keyboard_start.get_keyboard()

def create_applicant_keyboard():
    
    keyboard_applicant = VkKeyboard()

    # Добавляем кнопки
    keyboard_applicant.add_button('Редактировать ключевые слова', color=VkKeyboardColor.POSITIVE)
    keyboard_applicant.add_line()
    keyboard_applicant.add_button('Просмотреть ключевые слова', color=VkKeyboardColor.POSITIVE)
    keyboard_applicant.add_line()
    keyboard_applicant.add_button('Пример слов', color=VkKeyboardColor.POSITIVE)
    keyboard_applicant.add_line()
    keyboard_applicant.add_button('Отменить подписку', color=VkKeyboardColor.NEGATIVE)

    return keyboard_applicant.get_keyboard()

#sql запросы
def set_status(user_id, status, group_id):
   
    if group_id == 22156807:
        table = "kzn_users"
    if group_id == 220670949:
        table = "chlb_users"
    
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    # Запрос для обновления статуса по user_id
    update_status_query = f'''
    UPDATE {table}
    SET status = ?
    WHERE user_id = ?;
    '''
    # Выполнение запроса с передачей параметров new_status и user_id
    cursor.execute(update_status_query, (status, user_id))
    # Сохранение изменений и закрытие подключения к базе данных
                
    conn.commit()
    conn.close()

def set_keywords(user_id, keywords, group_id):
    
    if group_id == 22156807:
        table = "kzn_users"
    if group_id == 220670949:
        table = "chlb_users"

    keywords = keywords.lower()

    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    # Запрос для обновления ключевых слов
    update_status_query = f'''
    UPDATE {table}
    SET keywords = ?
    WHERE user_id = ?;
    '''
    cursor.execute(update_status_query, (keywords, user_id))
    # Сохранение изменений и закрытие подключения к базе данных
    conn.commit()
    conn.close()

def add_user(user_id, group_id):

    if group_id == 22156807:
        table = "kzn_users"
    if group_id == 220670949:
        table = "chlb_users"

    #подключение в базе данных 
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    #запрос на добавление нового юзера со статусом по умолчанию - start 
    add_user_query = f'''
    INSERT INTO {table} (user_id, status)
    VALUES (?, ?);
    '''
    #Выполнение запроса с передачей параметров user_id и status
    cursor.execute(add_user_query, (user_id, "start"))
    # Сохранение изменений и закрытие подключения к базе данных
    conn.commit()
    conn.close()

def remove_keywords(user_id, group_id):

    if group_id == 22156807:
        table = "kzn_users"
    if group_id == 220670949:
        table = "chlb_users"

    # Подключение к базе данных
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    # Запрос для очистки поля key_word по user_id
    clear_keyword_query = f'''
    UPDATE {table}
    SET keywords = NULL
    WHERE user_id = ?;
    '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(clear_keyword_query, (user_id,))
    # Сохранение изменений и закрытие подключения к базе данных
    conn.commit()
    conn.close()

def get_keywords(user_id, group_id):

    if group_id == 22156807:
        table = "kzn_users"
    if group_id == 220670949:
        table = "chlb_users"

    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    # Запрос для получения ключевых слов по user_id
    get_keywords_query = f'''
    SELECT keywords
    FROM {table}
    WHERE user_id = ? AND keywords IS NOT NULL;
    '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(get_keywords_query, (user_id,))
    result = cursor.fetchone()
    # Закрытие подключения к базе данных
    conn.close()
    return result

def get_status(user_id, group_id):

    if group_id == 22156807:
        table = "kzn_users"
    if group_id == 220670949:
        table = "chlb_users"

    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()

    # Запрос для проверки наличия записи с заданным user_id
    check_user_query = f'''
    SELECT EXISTS (
        SELECT 1
        FROM {table}
        WHERE user_id = ?
        LIMIT 1
    );
    '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(check_user_query, (user_id,))
    result = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    
    if result == 1:
       conn = sqlite3.connect('subscriptions.db')
       cursor = conn.cursor()
       # Запрос для получения статуса по user_id
       get_status_query = f'''
       SELECT status
       FROM {table}
       WHERE user_id = ?;
       '''
       # Выполнение запроса с передачей параметра user_id
       cursor.execute(get_status_query, (user_id,))
       status = cursor.fetchone()

       conn.commit()
       conn.close()

       return status
    
    else:
       return "0"

#созданию соединения
def create_connection():
    connection = sqlite3.connect('subscriptions.db')
    cursor = connection.cursor()

    # Создаем таблицу для хранения подписок пользователей, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS kzn_users
                      (user_id INTEGER PRIMARY KEY, keywords TEXT, status TEXT)''')

    connection.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS chlb_users
                      (user_id INTEGER PRIMARY KEY, keywords TEXT, status TEXT)''')

    connection.commit()
    connection.close()

#обработка сообщений, учитывая статус юзера, каждая функция должна возвращать текст ответа, клавиутуру, необходимость уведомить админа
def start_status_handler(user_id, message_text, group_id):
    
    
    if message_text == 'Хочу разместить вакансию':
        
        set_status(user_id=user_id, status="employer", group_id=group_id)
        
        return 'Сейчас вам ответит администратор!', None, True

    elif message_text == 'Ищу работу':
        
        set_status(user_id=user_id, status="applicant", group_id=group_id)
        
        return 'Выберите действие на клавиатуре:', create_applicant_keyboard(), None

    else:

        return 'Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', create_start_keyboard(), None
    

def employer_status_handler(user_id, message_text, group_id):

    if message_text == "/start": #откат до статуса старт

        set_status(user_id=user_id, status="start", group_id=group_id)

        return 'Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', create_start_keyboard(), None
    
    else:
        return None, None, True #бот не обрабатывает сообщение, уведомляет админа 

def editing_status_handler(user_id, message_text, group_id):
    
    if message_text == "/start":

        remove_keywords(user_id=user_id, group_id=group_id)
        set_status(user_id=user_id, status="start", group_id=group_id)
        return 'Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', create_start_keyboard(), None
    
    elif message_text == "" or message_text == "Отменить подписку":

        remove_keywords(user_id=user_id, group_id=group_id)
        set_status(user_id=user_id, status="applicant", group_id=group_id)  
        return "Подписка отменена!", None, None
    
    else:
        set_keywords(user_id=user_id,keywords=message_text, group_id=group_id)
        set_status(user_id=user_id, status="applicant", group_id=group_id)   
        return "Подписка по вашим ключевым словам - активна!", None, None

def applicant_status_handler(user_id, message_text, group_id):
   
    if message_text == "/start": #откат до статуса старт
        
        remove_keywords(user_id=user_id, group_id=group_id)
        set_status(user_id=user_id, status="start", group_id=group_id) 
        return 'Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', create_start_keyboard(), None
    
    elif message_text == "Редактировать ключевые слова":
        
        set_status(user_id=user_id, status="editing", group_id=group_id)
        return "Отправьте ключевые слова через запятую", None, None

    elif message_text == "Просмотреть ключевые слова":
        
        words = get_keywords(user_id=user_id, group_id=group_id)
        if words:
            return words[0], None, None
        else:
            return "У вас нет ключевых слов для подписки :(", None, None

    elif message_text == "Пример слов":
        return "без опыта, официант, бармен, подработка, стройка, шабашка, оплата сразу", None, None

    elif message_text == "Отменить подписку":

        remove_keywords(user_id=user_id, group_id=group_id)
        return "Подписка отменена!", None, None

    else:
        return 'Выберите действие на клавиатуре:', create_applicant_keyboard(), None

def none_status_handler(user_id, message_text, group_id):
    
    if message_text == '/start':
         
        add_user(user_id=user_id, group_id=group_id) #запись нового пользователя в бд, статус по умочланию = start
        return 'Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', create_start_keyboard(), None
        
    else: 
        return "Чтобы запустить бота, введите команду '/start'." , None, None
        
#обработка поста, возвращает id юзеров с совпадениями
def post_handler(post): # хз как это работает, chatgpt наебенил

    group_id = post.owner_id

    if group_id == -22156807:
        table = "kzn_users"
    if group_id == -220670949:
        table = "chlb_users"    
    

    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    
    # Разделение ключевых слов на отдельные слова
    keywords = [word.strip() for word in post.text.replace(',', ' ').split()]

    keywords = [word.lower() for word in keywords]

    # Создание временной таблицы для ключевых слов
    cursor.execute("CREATE TEMP TABLE keywords (key_word TEXT);")
    for keyword in keywords:
        cursor.execute("INSERT INTO keywords (key_word) VALUES (?);", (keyword, ))
    
    # Запрос для поиска совпадений
    find_matching_users_query = f'''
    SELECT DISTINCT user_id
    FROM {table}
    WHERE EXISTS (
        SELECT 1
        FROM keywords
        WHERE INSTR(LOWER({table}.keywords), LOWER(keywords.key_word)) > 0
    );
    '''

    # Выполнение запроса
    result = cursor.execute(find_matching_users_query).fetchall()

    # Извлечение значений user_id из результата запроса
    matching_users = [row[0] for row in result]
    print("Пользователи с совпадениями:", matching_users)
    # Закрытие подключения к базе данных
    conn.close()

    return matching_users

#обработка входящего сообщения, возвращает текст ответа, клавиатуру, необходимость уведомить админа
def reply_message_handler(event):
    
    group_id = event.group_id
    user_id = event.message.from_id
    message_text = event.message.text

    status = get_status(user_id=user_id, group_id=group_id)[0]
        
    if status == "start":
        
        response, keybord, notify = start_status_handler(user_id=user_id,message_text=message_text, group_id=group_id)

    elif status == "employer":
        
        response, keybord, notify = employer_status_handler(user_id=user_id,message_text=message_text, group_id=group_id)

    elif status == "applicant":

        response, keybord, notify = applicant_status_handler(user_id=user_id,message_text=message_text, group_id=group_id)

    elif status == "editing":
        
        response, keybord, notify = editing_status_handler(user_id=user_id,message_text=message_text, group_id=group_id)

    else:

        response, keybord, notify = none_status_handler(user_id=user_id,message_text=message_text, group_id=group_id)
        
    return response, keybord, notify

def main():

    print()


if __name__ == "__main__":
    main()

