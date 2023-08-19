import sqlite3

def main(): #обработчик любого сообщения в тг боте
     
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()

    your_text = "Путешествие – это уникальная пупа возможность уйти от повседневной рутины, лупа исследовать новые места и погрузиться в разнообразие культур и природных красот. Открывая перед собой неизведанные горизонты, мы встречаем удивительных людей, узнаем истории и традиции, которые делают каждое путешествие неповторимым."

    # Разделение ключевых слов на отдельные слова
    keywords = [word.strip() for word in your_text.replace(',', ' ').split()]

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
        WHERE INSTR(LOWER(users.key_word), LOWER(keywords.key_word)) > 0
    );
    '''

    # Выполнение запроса
    result = cursor.execute(find_matching_users_query).fetchall()

    # Извлечение значений user_id из результата запроса
    matching_users = [row[0] for row in result]
    print("Пользователи с совпадениями:", matching_users)
    # Закрытие подключения к базе данных
    conn.close()


if __name__ == '__main__':
    main()
