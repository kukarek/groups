import requests
import schedule
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Глобальный словарь для хранения предыдущих данных о монетах
prev_data = {}

def get_coin_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'percent_change_24h',
        'per_page': 10,
        'page': 1,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Ошибка при получении данных")
        return None

def check_coin_prices():
    data = get_coin_data()

    if data:
        for coin in data:
            name = coin['name']
            price_change_percentage = coin['price_change_percentage_24h']
            if name in prev_data and abs(price_change_percentage - prev_data[name]) > 10:
                message = f"Цена монеты {name} изменилась на {price_change_percentage:.2f}% за сутки!"
                send_notification(message)

            # Обновляем данные о предыдущей цене монеты
            prev_data[name] = price_change_percentage

def send_notification(message):
    # Ваш токен для бота
    bot_token = "6470735932:AAHG7LzA_VtGZvmK5JopIMqoiNa3CmuEvuM"
    # Ваш ID чата в телеграм (можно получить у @userinfobot)
    chat_id = "1020541698"

    updater = Updater(bot_token)
    updater.bot.send_message(chat_id=chat_id, text=message)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Я телеграм-бот, который будет отслеживать изменения цен криптовалют. "
                              "Для проверки текущих изменений введите /coins.")

def coins(update: Update, context: CallbackContext) -> None:
    data = get_coin_data()

    if data:
        response = "Текущие изменения цен криптовалют:\n"
        for coin in data:
            name = coin['name']
            price_change_percentage = coin['price_change_percentage_24h']
            response += f"{name}: {price_change_percentage:.2f}%\n"

        update.message.reply_text(response)

def main():
    # Ваш токен для бота
    bot_token = "6470735932:AAHG7LzA_VtGZvmK5JopIMqoiNa3CmuEvuM"

    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("coins", coins))

    # Запускаем расписание для периодической проверки
    schedule.every(5).minutes.do(check_coin_prices)

    # Запускаем бота
    updater.start_polling()

    # Отслеживаем расписание и запускаем бота бесконечно
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
