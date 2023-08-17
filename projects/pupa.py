from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Укажите токен VK бота и Telegram бота
VK_TOKEN = "vk1.a.qpY3UvDhUjNx20an2VW7vC4C5KvcZ6sPIESA8EFjKHPjivnEriP9ToosXqvf_DfGgK_Qws9dA429c1GXFmdhDNlHUJfnIYe0yl-E1cl0uXf6a8XCUTcFFvMSaMSd9FAYIqM7GxiYfamEEwTFpjNuUoaK77P_0_fFpwhIeEl-rOf2FspO_XdHWJPilQk0BwZV4drYCsQaKRXnml0PtfwQrQ"
TELEGRAM_TOKEN = "6470735932:AAHG7LzA_VtGZvmK5JopIMqoiNa3CmuEvuM"
CHANNEL_ID = "-1001948046451"  # Замените на свой канал

# Инициализация VK бота
vk_session = VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, "221134261")  # Замените на ваш ID группы

# Инициализация Telegram бота
telegram_bot = Bot(TELEGRAM_TOKEN)


def send_to_telegram(bot, update):
    message = update.message.text
    photos = update.message.photo  # Получение списка объектов фотографий

    if photos:
        # Если сообщение содержит изображения, отправляем их в Telegram
        for photo in photos:
            file_id = photo.file_id
            bot.send_photo(chat_id=CHANNEL_ID, photo=file_id, caption=message)
    else:
        # Если сообщение не содержит изображения, отправляем только текст
        bot.send_message(chat_id=CHANNEL_ID, text=message)


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
            if len(message) < 4095:

                attachments = event.object.attachments

                if attachments and "photo" in attachments[0]:
                    # Если в записи есть изображения, получаем ссылку на изображение
                    photo_url = attachments[0]["photo"]["sizes"][-1]["url"]
                    telegram_bot.send_photo(chat_id=CHANNEL_ID, photo=photo_url, caption=message)
                else:
                    # Если в записи нет изображений, отправляем только текст
                    telegram_bot.send_message(chat_id=CHANNEL_ID, text=message)


if __name__ == '__main__':
    main()
