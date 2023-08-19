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
def set_status(user_id, status):
   
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    # Запрос для обновления статуса по user_id
    update_status_query = '''
    UPDATE users
    SET status = ?
    WHERE user_id = ?;
    '''
    # Выполнение запроса с передачей параметров new_status и user_id
    cursor.execute(update_status_query, (status, user_id))
    # Сохранение изменений и закрытие подключения к базе данных
                
    conn.commit()
    conn.close()

def set_keywords(user_id, keywords):

    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    # Запрос для обновления ключевых слов
    update_status_query = '''
    UPDATE users
    SET keywords = ?
    WHERE user_id = ?;
    '''
    cursor.execute(update_status_query, (keywords, user_id))
    # Сохранение изменений и закрытие подключения к базе данных
    conn.commit()
    conn.close()

def add_user(user_id):
    #подключение в базе данных 
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    #запрос на добавление нового юзера со статусом по умолчанию - start 
    add_user_query = '''
    INSERT INTO users (user_id, status)
    VALUES (?, ?);
    '''
    #Выполнение запроса с передачей параметров user_id и status
    cursor.execute(add_user_query, (user_id, "start"))
    # Сохранение изменений и закрытие подключения к базе данных
    conn.commit()
    conn.close()

def remove_keywords(user_id):
    # Подключение к базе данных
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    # Запрос для очистки поля key_word по user_id
    clear_keyword_query = '''
    UPDATE users
    SET keywords = NULL
    WHERE user_id = ?;
    '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(clear_keyword_query, (user_id,))
    # Сохранение изменений и закрытие подключения к базе данных
    conn.commit()
    conn.close()

def get_keywords(user_id):

    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    # Запрос для получения ключевых слов по user_id
    get_keywords_query = '''
    SELECT keywords
    FROM users
    WHERE user_id = ? AND keywords IS NOT NULL;
    '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(get_keywords_query, (user_id,))
    result = cursor.fetchone()
    # Закрытие подключения к базе данных
    conn.close()
    return result

def get_status(user_id):

    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()

    # Запрос для проверки наличия записи с заданным user_id
    check_user_query = '''
    SELECT EXISTS (
        SELECT 1
        FROM users
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
       get_status_query = '''
       SELECT status
       FROM users
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
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (user_id INTEGER PRIMARY KEY, keywords TEXT, status TEXT)''')

    connection.commit()
    return connection

#обработка сообщений, учитывая статус юзера, каждая функция должна возвращать текст ответа, клавиутуру, необходимость уведомить админа
def start_status_handler(user_id, message_text):
    
    if message_text == 'Хочу разместить вакансию':
        
        set_status(user_id=user_id, status="employer")
        
        return 'Сейчас вам ответит администратор!', None, True

    elif message_text == 'Ищу работу':
        
        set_status(user_id=user_id, status="applicant")
        
        return 'Выберите действие на клавиатуре:', create_applicant_keyboard(), None

    else:

        return 'Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', create_start_keyboard(), None
    

def employer_status_handler(user_id, message_text):

    if message_text == "/start": #откат до статуса старт

        set_status(user_id=user_id, status="start")

        return 'Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', create_start_keyboard(), None
    
    else:
        return None, None, True #бот не обрабатывает сообщение, уведомляет админа 

def editing_status_handler(user_id, message_text):
    
    if message_text == "/start":

        remove_keywords(user_id=user_id)
        set_status(user_id=user_id, status="start")
        return 'Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', create_start_keyboard(), None
    
    elif message_text == "" or message_text == "Отменить подписку":

        remove_keywords(user_id=user_id)
        set_status(user_id=user_id, status="applicant")  
        return "Подписка отменена!", None, None
    
    else:
        set_keywords(user_id=user_id,keywords=message_text)
        set_status(user_id=user_id, status="applicant")   
        return "Подписка по вашим ключевым словам - активна!", None, None

def applicant_status_handler(user_id, message_text):
   
    if message_text == "/start": #откат до статуса старт
        
        remove_keywords(user_id=user_id)
        set_status(user_id=user_id, status="start") 
        return 'Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', create_start_keyboard(), None
    
    elif message_text == "Редактировать ключевые слова":
        
        set_status(user_id=user_id, status="editing")
        return "Отправьте ключевые слова через запятую", None, None

    elif message_text == "Просмотреть ключевые слова":
        
        words = get_keywords(user_id=user_id)
        if words:
            return words[0], None, None
        else:
            return "У вас нет ключевых слов для подписки :(", None, None

    elif message_text == "Пример слов":
        return "без опыта, официант, бармен, подработка, стройка, шабашка, оплата сразу", None, None

    elif message_text == "Отменить подписку":

        remove_keywords(user_id=user_id)
        return "Подписка отменена!", None, None

    else:
        return 'Выберите действие на клавиатуре:', create_applicant_keyboard(), None

def none_status_handler(user_id, message_text):
    
    if message_text == '/start':
         
        add_user(user_id=user_id) #запись нового пользователя в бд, статус по умочланию = start
        return 'Выберите на клавиатуре, вы хотите разместить вакансию или ищете работу?', create_start_keyboard(), None
        
    else: 
        return "Чтобы запустить бота, введите команду '/start'." , None, None
        
#обработка поста, возвращает id юзеров с совпадениями
def post_handler(post): # хз как это работает, chatgpt наебенил

    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    
    # Разделение ключевых слов на отдельные слова
    keywords = [word.strip() for word in post.text.replace(',', ' ').split()]

    # Создание временной таблицы для ключевых слов
    cursor.execute("CREATE TEMP TABLE keywords (key_word TEXT);")
    for keyword in keywords:
        cursor.execute("INSERT INTO keywords (key_word) VALUES (?);", (keyword, ))
    
    # Запрос для поиска совпадений
    find_matching_users_query = '''
    SELECT DISTINCT user_id
    FROM users
    WHERE EXISTS (
        SELECT 1
        FROM keywords
        WHERE INSTR(LOWER(users.keywords), LOWER(keywords.key_word)) > 0
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

    user_id = event.message.from_id
    message_text = event.message.text

    status = get_status(user_id=user_id)[0]
        
    if status == "start":
        
        response, keybord, notify = start_status_handler(user_id=user_id,message_text=message_text)

    elif status == "employer":
        
        response, keybord, notify = employer_status_handler(user_id=user_id,message_text=message_text)

    elif status == "applicant":

        response, keybord, notify = applicant_status_handler(user_id=user_id,message_text=message_text)

    elif status == "editing":
        
        response, keybord, notify = editing_status_handler(user_id=user_id,message_text=message_text)

    else:

        response, keybord, notify = none_status_handler(user_id=user_id,message_text=message_text)
        
    return response, keybord, notify

def main():

    print()


if __name__ == "__main__":
    main()

