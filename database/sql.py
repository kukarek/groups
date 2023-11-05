import sqlite3
from misc.config import db

#sql запросы
def set_status(user_id, status, group_id):

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    # Запрос для обновления статуса по user_id
    update_status_query = f'''
    UPDATE group_{group_id}
    SET status = ?
    WHERE user_id = ?;
    '''
    # Выполнение запроса с передачей параметров new_status и user_id
    cursor.execute(update_status_query, (status, user_id))
    # Сохранение изменений и закрытие подключения к базе данных
                
    conn.commit()
    conn.close()

def set_tg_user_status(user_id, status):
   
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    update_status_query = f'''
    UPDATE users
    SET status = ?
    WHERE user_id = ?;
    '''
    cursor.execute(update_status_query, (status, user_id))
            
    conn.commit()
    conn.close()

def set_tg_user_current_group(user_id, current_group_id):
   
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    query = f'''
    UPDATE users
    SET current_group_id = ?
    WHERE user_id = ?;
    '''
    cursor.execute(query, (current_group_id, user_id))
            
    conn.commit()
    conn.close()

def add_tg_user(user_id):

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Запрос для проверки наличия записи с заданным user_id
    query = f'''
    INSERT INTO users (user_id)
    VALUES (?);
    '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(query, (user_id,))

    conn.commit()
    conn.close()

def check_tg_user(user_id):

    conn = sqlite3.connect(db)
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

    return result

def set_keywords(user_id, keywords, group_id):
    
    keywords = keywords.lower()

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    # Запрос для обновления ключевых слов
    update_status_query = f'''
    UPDATE group_{group_id}
    SET keywords = ?
    WHERE user_id = ?;
    '''
    cursor.execute(update_status_query, (keywords, user_id))
    # Сохранение изменений и закрытие подключения к базе данных
    conn.commit()
    conn.close()

def add_user(user_id, group_id):

    #подключение в базе данных 
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    #запрос на добавление нового юзера со статусом по умолчанию - start 
    add_user_query = f'''
    INSERT INTO group_{group_id} (user_id, status)
    VALUES (?, ?);
    '''
    #Выполнение запроса с передачей параметров user_id и status
    cursor.execute(add_user_query, (user_id, "start"))
    # Сохранение изменений и закрытие подключения к базе данных
    conn.commit()
    conn.close()

def remove_keywords(user_id, group_id):

    # Подключение к базе данных
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    # Запрос для очистки поля key_word по user_id
    clear_keyword_query = f'''
    UPDATE group_{group_id}
    SET keywords = NULL
    WHERE user_id = ?;
    '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(clear_keyword_query, (user_id,))
    # Сохранение изменений и закрытие подключения к базе данных
    conn.commit()
    conn.close()

def get_keywords(user_id, group_id):

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    # Запрос для получения ключевых слов по user_id
    get_keywords_query = f'''
    SELECT keywords
    FROM group_{group_id}
    WHERE user_id = ? AND keywords IS NOT NULL;
    '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(get_keywords_query, (user_id,))
    result = cursor.fetchone()
    # Закрытие подключения к базе данных
    conn.close()
    return result

def get_status(user_id, group_id):

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Запрос для проверки наличия записи с заданным user_id
    check_user_query = f'''
    SELECT EXISTS (
        SELECT 1
        FROM group_{group_id}
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
       FROM group_{group_id}
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
    
def get_tg_user_status(user_id):

    conn = sqlite3.connect(db)
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

    if status == None:
        return None
    else:
        return status[0]

def get_tg_user_current_group(user_id):

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    # Запрос для получения статуса по user_id
    query = f'''
    SELECT current_group_id
    FROM users
    WHERE user_id = ?;
    '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(query, (user_id,))
    status = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return status
    
def get_users_data_as_dict(group_id): 

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    select_users_query = f'''
    SELECT user_id, keywords
    FROM group_{group_id}
    WHERE keywords IS NOT NULL;
    '''

    cursor.execute(select_users_query)
    user_data_rows = cursor.fetchall()

    users_data = [{"user_id": row[0], "keywords": row[1]} for row in user_data_rows]

    conn.close()
    return users_data

def create_group_users_table(group_id):

    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS group_{group_id}
                      (user_id INTEGER PRIMARY KEY, status TEXT, keywords TEXT)''')

    connection.commit()
    connection.close()
    
def add_vk_admin(group_id, admin_id):

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Запрос для получения списка админов по group_id
    query = f'''
    SELECT VK_ADMINS
    FROM groups
    WHERE group_id = ?;
    '''
    
    cursor.execute(query, (group_id,))
    admins = cursor.fetchone()[0]


    update_admins = ""

    if admins:
        update_admins = admins + f", {admin_id}"
    else:
        update_admins = admin_id


    # Запрос для обновления списка админов
    query = f'''
    UPDATE groups
    SET VK_ADMINS = ?
    WHERE group_id = ?;
    '''

    cursor.execute(query, (update_admins, group_id))
    # Сохранение изменений и закрытие подключения к базе данных
    conn.commit()
    conn.close()

def set_group_value(group_id, value_key, value):

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Запрос для обновления списка админов
    query = f'''
    UPDATE groups
    SET {value_key} = ?
    WHERE group_id = ?;
    '''

    cursor.execute(query, (value, group_id))
    # Сохранение изменений и закрытие подключения к базе данных
    conn.commit()
    conn.close()

def add_group(group_id, user_id):

    #подключение в базе данных 
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    #запрос на добавление нового юзера со статусом по умолчанию - start 
    add_user_query = f'''
    INSERT INTO groups (group_id, user_id)
    VALUES (?, ?);
    '''
    #Выполнение запроса с передачей параметров user_id и status
    cursor.execute(add_user_query, (group_id, user_id))
    # Сохранение изменений и закрытие подключения к базе данных
    conn.commit()
    conn.close()

def get_vk_admins(group_id):

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    query = f'''
    SELECT VK_ADMINS
    FROM groups
    WHERE group_id = ?;
    '''
    
    cursor.execute(query, (group_id,))
    result = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return result.split(", ")

def remove_vk_admin(current_group_id, admin_id):

    admins = get_vk_admins(current_group_id)
    
    update_admins = ""

    result = False

    for admin in admins:
        if admin != admin_id:
            if update_admins == "":
                update_admins += admin
            else:
                update_admins += f", {admin}"
        else:
            result = True

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Запрос для обновления списка админов
    query = f'''
    UPDATE groups
    SET VK_ADMINS = ?
    WHERE group_id = ?;
    '''

    cursor.execute(query, (update_admins, current_group_id))
    # Сохранение изменений и закрытие подключения к базе данных
    conn.commit()
    conn.close()

    return result

            

def get_group_ids():

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    query = f'''
    SELECT group_id
    FROM groups
    '''

    cursor.execute(query)
    groups_data_rows = cursor.fetchall()

    group_ids = [row[0] for row in groups_data_rows]

    conn.close()

    return group_ids

def get_group_data(group_id):

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    query = f'''
    SELECT GROUP_NAME, VK_TOKEN, VK_TOKEN_FOR_DELAY, user_id, example_words, rules_link, payment
    FROM groups
    WHERE group_id = ?
    '''

    cursor.execute(query, (group_id,))
    group_data_rows = cursor.fetchall()[0]

    group_data = {
        "GROUP_NAME": group_data_rows[0],
        "VK_TOKEN": group_data_rows[1],
        "VK_TOKEN_FOR_DELAY": group_data_rows[2],
        "OWNER_ID": group_data_rows[3],
        "example_words": group_data_rows[4],
        "rules_link": group_data_rows[5],
        "payment": group_data_rows[6]
     }

    conn.close()

    return group_data

def get_current_group_id(user_id):

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    # Запрос для получения статуса по user_id
    query = f'''
    SELECT current_group_id
    FROM users
    WHERE user_id = ?;
    '''
    # Выполнение запроса с передачей параметра user_id
    cursor.execute(query, (user_id,))
    group_id = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return group_id

def set_current_group(user_id, current_group_id):

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    query = f'''
    UPDATE users
    SET current_group_id = ?
    WHERE user_id = ?;
    '''
    
    cursor.execute(query, (current_group_id, user_id))

    conn.commit()
    conn.close()

def remove_group(group_id):

    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM groups WHERE group_id=?", (group_id,))

    cursor.execute(f"DROP TABLE IF EXISTS group_{group_id}")

    connection.commit()
    connection.close()

def clean_invalid_groups():

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    query = f'''
    DELETE FROM groups
    WHERE group_id IS NULL OR
        GROUP_NAME IS NULL OR
        VK_TOKEN IS NULL OR
        VK_TOKEN_FOR_DELAY IS NULL OR
        VK_ADMINS IS NULL OR
        user_id IS NULL;
    '''

    cursor.execute(query)
    conn.commit()
    conn.close()

#создание бд
def create_connection():    
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (user_id INTEGER PRIMARY KEY, status TEXT, current_group_id TEXT)''')
    

    cursor.execute('''CREATE TABLE IF NOT EXISTS groups
                      (group_id INTEGER PRIMARY KEY,
                       GROUP_NAME TEXT, 
                       VK_TOKEN TEXT, 
                       VK_TOKEN_FOR_DELAY TEXT,
                       VK_ADMINS TEXT,
                       user_id INTEGER,
                       example_words TEXT, 
                       rules_link TEXT,
                       payment TEXT)''')

    connection.commit()
    connection.close()
