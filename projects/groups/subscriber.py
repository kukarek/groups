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
    keyboard_applicant.add_button('Просмотреть ключевые слова', color=VkKeyboardColor.POSITIVE)
    keyboard_applicant.add_button('Пример ключевых слов', color=VkKeyboardColor.POSITIVE)
    keyboard_applicant.add_button('Отменить подписку', color=VkKeyboardColor.NEGATIVE)

    return keyboard_applicant.get_keyboard()


def create_connection():
    connection = sqlite3.connect('subscriptions.db')
    cursor = connection.cursor()

    # Создаем таблицу для хранения подписок пользователей, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS subscriptions
                      (user_id INTEGER PRIMARY KEY, keywords TEXT)''')

    connection.commit()
    return connection

def insert_subscription(connection, user_id, keywords):
    cursor = connection.cursor()
    cursor.execute('INSERT OR REPLACE INTO subscriptions (user_id, keywords) VALUES (?, ?)', (user_id, keywords))
    connection.commit()

def get_subscription(connection, user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT keywords FROM subscriptions WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def search_users():
    
    print()

def start_status_handler():
    
    print()

def employer_status_handler():
    
    print()

def editing_status_handler():
    
    print()    

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

    return matching_users


def reply_message_handler(user_id, message_text):
    conn = create_connection()
    cursor = conn.cursor()




    conn.commit()
    conn.close()
    cursor.close()



def main():
    

   

            if "," in message:
                keywords = [word.strip() for word in message.split(",")]
                # Сохраняем ключевые слова для подписки в базу данных
                keywords_str = ", ".join(keywords)
                insert_subscription(connection, user_id, keywords_str)
                response = "Вы успешно оформили подписку на ключевые слова:\n" + ", ".join(keywords)
                send_text_message(vk, user_id, response)

            elif "привет" in message.lower():
                response = ("Доброго времени суток, у вас есть возможность абсолютно бесплатно оформить подписку "
                            "на интересующую вас тематику, и как только будут опубликованы объявления с нужным содержимым, "
                            "вы сразу получите их сообщением)")
                send_text_message(vk, user_id, response)

            elif "хорошо, спасибо!" in message.lower():
                response = "Буду рад помочь!"
                send_text_message(vk, user_id, response)

            elif "давай попробуем" in message.lower():
                response = "Введите ключевые слова для подписки через запятую (например, работа, квартира, авто):"
                send_text_message(vk, user_id, response)

            elif "отменить подписку" in message.lower():
                response = "Вы успешно отменили подписку."
                # Здесь можно добавить логику отмены подписки для конкретного пользователя
                send_text_message(vk, user_id, response)

            else:
                response = "Простите, я не понимаю вашего запроса. Попробуйте снова."
                send_text_message(vk, user_id, response)

            if "привет" in message.lower():
                response = ("Доброго времени суток, у вас есть возможность абсолютно бесплатно оформить подписку "
                            "на интересующую вас тематику, и как только будут опубликованы объявления с нужным содержимым, "
                            "вы сразу получите их сообщением)")
                send_text_message_with_keyboard(vk, user_id, response, keyboard)


            elif event.type == VkBotEventType.WALL_POST_NEW:
            # Обработка новых постов на стене, как было ранее
               post_id = event.obj.get('id')
               if post_id is not None and post_id > get_last_post_id(connection, group_id):
                # Получаем текст поста
                post_text = event.obj.get('text')

                # Проверяем, соответствует ли пост ключевым словам подписчиков
                cursor = connection.cursor()
                cursor.execute('SELECT user_id, keywords FROM subscriptions')
                subscribers = cursor.fetchall()

                for subscriber in subscribers:
                     user_id, keywords = subscriber
                     if keywords and any(keyword.lower() in post_text.lower() for keyword in keywords.split(',')):
                        # Отправляем пост подписчику, если есть соответствие
                        try:
                            random_id = random.randint(1, 10**9)
                            vk.messages.send(user_id=user_id, random_id=random_id)
                            print(f"Пост отправлен подписчику {user_id}")
                        except vk_api.VkApiError as e:
                            print(f"Ошибка при отправке поста пользователю {user_id}: {e}")

                # Обновляем последний ID поста в базе данных
                set_last_post_id(connection, group_id, post_id)


if __name__ == "__main__":
    main()

