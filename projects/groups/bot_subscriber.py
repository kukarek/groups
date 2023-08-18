import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlite3
import random


def create_start_keyboard():
    # Создаем клавиатуру
    keyboard_start = VkKeyboard(one_time=True)

    # Добавляем кнопки
    keyboard_start.add_button('Хочу разместить вакансию', color=VkKeyboardColor.POSITIVE)
    keyboard_start.add_button('Ищу работу', color=VkKeyboardColor.POSITIVE)

    return keyboard_start.get_keyboard()

def create_applicant_keyboard():
    # Создаем клавиатуру
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

