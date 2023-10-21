import sqlite3
from misc.config import db
#sql запросы
def set_status(user_id, status, group_id):
   
    if group_id == 22156807:
        table = "kzn_users"
    if group_id == 220670949:
        table = "chlb_users"
    
    conn = sqlite3.connect(db)
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

    conn = sqlite3.connect(db)
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
    conn = sqlite3.connect(db)
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
    conn = sqlite3.connect(db)
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

    conn = sqlite3.connect(db)
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

    conn = sqlite3.connect(db)
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
       conn = sqlite3.connect(db)
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
    
def get_users_data_as_dict(group_id): 
    
    if group_id == -22156807:
        table = "kzn_users"
    if group_id == -220670949:
        table = "chlb_users" 

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    select_users_query = f'''
    SELECT user_id, keywords
    FROM {table}
    WHERE keywords IS NOT NULL;
    '''

    cursor.execute(select_users_query)
    user_data_rows = cursor.fetchall()

    users_data = [{"user_id": row[0], "keywords": row[1]} for row in user_data_rows]

    conn.close()
    return users_data

#созданию соединения (не используется в коде)
def create_connection():
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    # Создаем таблицу для хранения подписок пользователей, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS kzn_users
                      (user_id INTEGER PRIMARY KEY, keywords TEXT, status TEXT)''')

    connection.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS chlb_users
                      (user_id INTEGER PRIMARY KEY, keywords TEXT, status TEXT)''')

    connection.commit()
    connection.close()
