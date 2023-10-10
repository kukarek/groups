import sqlite3

#sql запросы
def set_status(user_id, status):
   
    conn = sqlite3.connect('invatedusers.db')
    cursor = conn.cursor()
    # Запрос для обновления статуса по user_id
    update_status_query = f'''
    UPDATE users
    SET status = ?
    WHERE user_id = ?;
    '''
    # Выполнение запроса с передачей параметров new_status и user_id
    cursor.execute(update_status_query, (status, user_id))
    # Сохранение изменений и закрытие подключения к базе данных
                
    conn.commit()
    conn.close()

def set_phone(user_id, phone):
   
    conn = sqlite3.connect('invatedusers.db')
    cursor = conn.cursor()
    # Запрос для обновления статуса по user_id
    update_phone_query = f'''
    UPDATE users
    SET phone = ?
    WHERE user_id = ?;
    '''
    # Выполнение запроса с передачей параметров new_status и user_id
    cursor.execute(update_phone_query, (phone, user_id))
    # Сохранение изменений и закрытие подключения к базе данных
                
    conn.commit()
    conn.close()

def set_time(user_id, time):
   
    conn = sqlite3.connect('invatedusers.db')
    cursor = conn.cursor()
    # Запрос для обновления статуса по user_id
    update_time_query = f'''
    UPDATE users
    SET time = ?
    WHERE user_id = ?;
    '''
    # Выполнение запроса с передачей параметров new_status и user_id
    cursor.execute(update_time_query, (time, user_id))
    # Сохранение изменений и закрытие подключения к базе данных
                
    conn.commit()
    conn.close()

def set_exp(user_id, exp):
   
    conn = sqlite3.connect('invatedusers.db')
    cursor = conn.cursor()
    # Запрос для обновления статуса по user_id
    update_exp_query = f'''
    UPDATE users
    SET exp = ?
    WHERE user_id = ?;
    '''
    # Выполнение запроса с передачей параметров new_status и user_id
    cursor.execute(update_exp_query, (exp, user_id))
    # Сохранение изменений и закрытие подключения к базе данных
                
    conn.commit()
    conn.close()

def set_lolz(user_id, lolz):
   
    conn = sqlite3.connect('invatedusers.db')
    cursor = conn.cursor()
    # Запрос для обновления статуса по user_id
    update_lolz_query = f'''
    UPDATE users
    SET lolz = ?
    WHERE user_id = ?;
    '''
    # Выполнение запроса с передачей параметров new_status и user_id
    cursor.execute(update_lolz_query, (lolz, user_id))
    # Сохранение изменений и закрытие подключения к базе данных
                
    conn.commit()
    conn.close()

def add_user(user_id):
    
    #подключение в базе данных 
    conn = sqlite3.connect('invatedusers.db')
    cursor = conn.cursor()
    #запрос на добавление нового юзера со статусом по умолчанию - start 
    add_user_query = f'''
    INSERT INTO users (user_id, status)
    VALUES (?, ?);
    '''
    #Выполнение запроса с передачей параметров user_id и status
    cursor.execute(add_user_query, (user_id, "phone"))
    # Сохранение изменений и закрытие подключения к базе данных
    conn.commit()
    conn.close()

def get_status(user_id):

    conn = sqlite3.connect('invatedusers.db')
    cursor = conn.cursor()

    # Запрос для проверки наличия записи с заданным user_id
    check_user_query = f'''
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
       conn = sqlite3.connect('invatedusers.db')
       cursor = conn.cursor()
       # Запрос для получения статуса по user_id
       get_status_query = f'''
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

def get_user_info(user_id):

    conn = sqlite3.connect('invatedusers.db')
    cursor = conn.cursor()

    # Запрос для проверки наличия записи с заданным user_id
    check_user_query = f'''
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
       conn = sqlite3.connect('invatedusers.db')
       cursor = conn.cursor()
       # Запрос для получения статуса по user_id
       get_status_query = f'''
       SELECT *
       FROM users
       WHERE user_id = ?;
       '''
       # Выполнение запроса с передачей параметра user_id
       cursor.execute(get_status_query, (user_id,))
       info = cursor.fetchone()

       conn.commit()
       conn.close()

       return info
    
    else:
       return "0"

#созданию соединения (не используется в коде)
def create_connection():
    connection = sqlite3.connect('invatedusers.db')
    cursor = connection.cursor()

    # Создаем таблицу для хранения подписок пользователей, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (user_id INTEGER PRIMARY KEY, status TEXT, phone TEXT, time TEXT, exp TEXT, lolz TEXT)''')

    connection.commit()
    connection.close()
