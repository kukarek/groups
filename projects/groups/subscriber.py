import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlite3
import random
"""
библиотека создана для того, чтобы обрабатывать входящие сообщения по user_id, status и message.text
status тянет из локальной бд 
здесь происходит все взамодействие с бд 
принимает сообщение, определяет по статусу переписки ответ, возвращает ответ и id получателя
"""

def create_keyboard():
    # Создаем клавиатуру
    keyboard = VkKeyboard(one_time=True)

    # Добавляем кнопки
    keyboard.add_button('Хорошо, спасибо!', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Давай попробуем', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()  # Переход на вторую строку
    keyboard.add_button('Отменить подписку', color=VkKeyboardColor.NEGATIVE)

    return keyboard.get_keyboard()

def send_text_message_with_keyboard(vk, user_id, message, keyboard):
    try:
        random_id = random.randint(1, 10**9)
        vk.messages.send(user_id=user_id, message=message, random_id=random_id, keyboard=keyboard)
        print("Текстовое сообщение успешно отправлено!")
    except vk_api.VkApiError as e:
        print(f"Ошибка при отправке текстового сообщения: {e}")

def create_connection():
    connection = sqlite3.connect('subscriptions.db')
    cursor = connection.cursor()

    # Создаем таблицу для хранения подписок пользователей, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS subscriptions
                      (user_id INTEGER PRIMARY KEY, keywords TEXT)''')

    # Создаем таблицу для хранения последнего ID поста, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS last_post_id
                      (group_id TEXT PRIMARY KEY, post_id INTEGER)''')

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

def send_text_message(vk, user_id, message):
    try:
        random_id = random.randint(1, 10**9)
        vk.messages.send(user_id=user_id, message=message, random_id=random_id)
        print("Текстовое сообщение успешно отправлено!")
    except vk_api.VkApiError as e:
        print(f"Ошибка при отправке текстового сообщения: {e}")

def send_wall_post_to_subscribers(connection, vk, group_id, post_id):
    cursor = connection.cursor()
    cursor.execute('SELECT user_id, keywords FROM subscriptions')
    subscribers = cursor.fetchall()

    for subscriber in subscribers:
        user_id, keywords = subscriber
        if keywords:
            # Проверяем, соответствует ли пост ключевым словам подписчика
            post = vk.wall.getById(posts=f"{group_id}_{post_id}", extended=1)
            post_text = post[0]['text']
            if any(keyword.lower() in post_text.lower() for keyword in keywords.split(',')):
                # Пересылаем пост подписчику, если есть соответствие
                try:
                    random_id = random.randint(1, 10**9)
                    vk.messages.send(user_id=user_id, forward_messages=post_id, random_id=random_id)
                    print(f"Пост переслан подписчику {user_id}")
                except vk_api.VkApiError as e:
                    print(f"Ошибка при пересылке поста пользователю {user_id}: {e}")

    # Обновляем последний ID поста в базе данных
    set_last_post_id(connection, group_id, post_id)

    for subscriber in subscribers:
        user_id, keywords = subscriber
        if keywords:
            # Проверяем, соответствует ли пост ключевым словам подписчика
            try:
                code = f'''
                    var post = API.wall.getById({{"posts": "{group_id}_{post_id}"}})[0];
                    var post_text = post.text;
                    return post_text;
                '''

                response = vk.execute(code)

                post_text = response['response']

                # Преобразуем ключевые слова в список, разделенный запятыми
                keyword_list = [keyword.strip().lower() for keyword in keywords.split(',')]
            
                if any(keyword in post_text.lower() for keyword in keyword_list):
                    # Пересылаем пост подписчику, если есть соответствие
                    try:
                        attachments = f"wall{group_id}_{post_id}"
                        random_id = vk_api.utils.get_random_id()
                        vk.messages.send(user_id=user_id, attachment=attachments, random_id=random_id)
                        print(f"Запись со стены переслана подписчику {user_id}")
                    except vk_api.VkApiError as e:
                        print(f"Ошибка при пересылке записи со стены пользователю {user_id}: {e}")
            except vk_api.VkApiError as e:
                print(f"Ошибка при получении информации о посте со стены: {e}")

    # Обновляем последний ID поста в базе данных
    set_last_post_id(connection, group_id, post_id)

# Остальные функции остаются без изменений





def get_last_post_id(connection, group_id):
    cursor = connection.cursor()
    cursor.execute('SELECT post_id FROM last_post_id WHERE group_id = ?', (group_id,))
    result = cursor.fetchone()
    return result[0] if result else 0  # Возвращаем 0, если пост с последним ID не найден


def set_last_post_id(connection, group_id, post_id):
    cursor = connection.cursor()
    cursor.execute('INSERT OR REPLACE INTO last_post_id (group_id, post_id) VALUES (?, ?)', (group_id, post_id))
    connection.commit()

def main():
    connection = create_connection()

    # Вставьте ваш токен и ID группы ВКонтакте
    vk_token = 'vk1.a.qpY3UvDhUjNx20an2VW7vC4C5KvcZ6sPIESA8EFjKHPjivnEriP9ToosXqvf_DfGgK_Qws9dA429c1GXFmdhDNlHUJfnIYe0yl-E1cl0uXf6a8XCUTcFFvMSaMSd9FAYIqM7GxiYfamEEwTFpjNuUoaK77P_0_fFpwhIeEl-rOf2FspO_XdHWJPilQk0BwZV4drYCsQaKRXnml0PtfwQrQ'
    group_id = '221134261'

    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id)

    keyboard = create_keyboard()

    print("Бот запущен!")

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.obj.message['from_id']
            message = event.obj.message['text']

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

