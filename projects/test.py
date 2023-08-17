import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from telegram import Bot, Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# ... (Ваши токены VK и Telegram и другие настройки)
# Укажите токен VK бота и Telegram бота
VK_TOKEN = "vk1.a.qpY3UvDhUjNx20an2VW7vC4C5KvcZ6sPIESA8EFjKHPjivnEriP9ToosXqvf_DfGgK_Qws9dA429c1GXFmdhDNlHUJfnIYe0yl-E1cl0uXf6a8XCUTcFFvMSaMSd9FAYIqM7GxiYfamEEwTFpjNuUoaK77P_0_fFpwhIeEl-rOf2FspO_XdHWJPilQk0BwZV4drYCsQaKRXnml0PtfwQrQ"
TELEGRAM_TOKEN = "6470735932:AAHG7LzA_VtGZvmK5JopIMqoiNa3CmuEvuM"
CHANNEL_ID = "-1001948046451"  # Замените на свой канал

# Инициализация VK бота
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, "221134261")  # Замените на ваш ID группы



# Инициализация Telegram бота
telegram_bot = Bot(TELEGRAM_TOKEN)


def send_large_text(chat_id, text):
    max_length = 4000
    parts = [text[i:i + max_length] for i in range(0, len(text), max_length)]

    for i, part in enumerate(parts):
        telegram_bot.send_message(chat_id=chat_id, text=part)


def send_to_telegram(update: Update, context: CallbackContext):
    message = update.message.text
    photos = update.message.photo  # Получение списка объектов фотографий

    if photos and len(message) > 4000:
        # Если сообщение содержит и изображения и текст большой длины, разделяем и отправляем отдельно
        media_group = [InputMediaPhoto(photo.file_id, caption=message)]
        telegram_bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)

        remaining_text = message[len("".join([photo.file_id for photo in photos])):]  # Оставшийся текст после изображения
        send_large_text(chat_id=CHANNEL_ID, text=remaining_text)
    elif photos:
        # Если сообщение содержит только изображения, отправляем их как вложения
        for photo in photos:
            telegram_bot.send_photo(chat_id=CHANNEL_ID, photo=photo.file_id, caption=message)
    elif len(message) > 4000:
        # Если сообщение длинное, отправляем его в нескольких сообщениях
        send_large_text(chat_id=CHANNEL_ID, text=message)
    else:
        # Если сообщение небольшое, отправляем его как обычное текстовое сообщение
        telegram_bot.send_message(chat_id=CHANNEL_ID, text=message)


def main():
    updater = Updater(TELEGRAM_TOKEN)

    # Обработчики команд и сообщений от пользователя
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_to_telegram))

    # Запускаем обновления Telegram бота
    updater.start_polling()

    # Отслеживание новых записей на стене VK
    for event in longpoll.listen():
        if event.type == VkBotEventType.WALL_POST_NEW:
            message = event.object.text
            attachments = event.object.attachments

            photos = []
            if attachments:
                # Если в записи есть вложения, сохраняем изображения
                photos = [InputMediaPhoto(attachment["photo"]["sizes"][-1]["url"]) for attachment in attachments
                          if attachment["type"] == "photo"]

            if photos and len(message) > 4000:
                # Если сообщение содержит и изображения и текст большой длины, разделяем и отправляем отдельно
                media_group = [InputMediaPhoto(photo.file_id, caption=message)]
                telegram_bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)

                remaining_text = message[len("".join([photo.file_id for photo in photos])):]  # Оставшийся текст после изображения
                send_large_text(chat_id=CHANNEL_ID, text=remaining_text)
            elif photos:
                # Если сообщение содержит только изображения, отправляем их как вложения
                for photo in photos:
                    telegram_bot.send_photo(chat_id=CHANNEL_ID, photo=photo.file_id, caption=message)
            elif len(message) > 4000:
                # Если сообщение длинное, отправляем его в нескольких сообщениях
                send_large_text(chat_id=CHANNEL_ID, text=message)
            else:
                # Если сообщение небольшое, отправляем его как обычное текстовое сообщение
                telegram_bot.send_message(chat_id=CHANNEL_ID, text=message)


if __name__ == '__main__':
    main()
