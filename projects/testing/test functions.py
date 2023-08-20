import sqlite3


def get_users_data_as_dict():

    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()

    select_users_query = '''
    SELECT user_id, keywords
    FROM chlb_users
    WHERE keywords IS NOT NULL;
    '''

    cursor.execute(select_users_query)
    user_data_rows = cursor.fetchall()

    users_data = [{"user_id": row[0], "keywords": row[1]} for row in user_data_rows]

    conn.close()
    return users_data

def find_matching_users(users_data, post_text):
    matching_users = []

    for user in users_data:
        user_id = user['user_id']
        keywords = user['keywords']

        # Разделение ключевых слов на отдельные слова
        keyword_list = keywords.replace(',', ' ').split()

        for keyword in keyword_list:
            if keyword in post_text.lower():
                matching_users.append(user_id)
                break  # Для оптимизации - если слово найдено, выходим из внутреннего цикла

    return matching_users
def main():
# Пример использования
   users_data = [
    {"user_id": 1, "keywords": "apple, banana"},
    {"user_id": 2, "keywords": "orange, grape"},
    {"user_id": 3, "keywords": "cherry, lemon"},
   ]
   
   users_data = get_users_data_as_dict()
    
   external_text = "I love bananas and oranges. тест"

   result = find_matching_users(users_data, external_text)

   if result:
      print("Пользователи с совпадающими ключевыми словами:", result)
   else:
      print("Совпадающие пользователи не найдены.")


if __name__ == '__main__':
    main()
