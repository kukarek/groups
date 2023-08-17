import requests
import ccxt
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Ваш токен для бота
bot_token = "6470735932:AAHG7LzA_VtGZvmK5JopIMqoiNa3CmuEvuM"
# Ваш ID чата в телеграм (можно получить у @userinfobot)
chat_id = "1020541698"

def get_top_volatility_coins():
    exchange = ccxt.tradingview()
    markets = exchange.fetch_markets()

    data = []

    for market in markets:
        if "percentage" in market["info"]:
            # TradingView предоставляет процентное изменение за 1 день в поле "percentage"
            market["percentage"] = abs(market["info"]["percentage"])
            data.append(market)

    # Сортируем данные по волатильности (изменению цены за 1 день)
    sorted_coins = sorted(data, key=lambda x: x["percentage"], reverse=True)
    return sorted_coins[:10]  # Берем топ-10 самых волатильных монет

if __name__ == "__main__":
    top_coins = get_top_volatility_coins()

    if top_coins:
        print("Список десяти самых волатильных криптовалют:")
        for coin in top_coins:
            name = coin["symbol"]
            percentage = coin["percentage"]
            print(f"{name}: {percentage:.2f}%")

def send_top_volatility_coins(update: Update, context: CallbackContext):
    data = get_top_volatility_coins()

    if data:
        # Сортируем данные по волатильности (изменению цены за 24 часа)
        sorted_coins = sorted(data, key=lambda x: x["price_change_percentage_24h"], reverse=True)
        # Берем топ-10 самых волатильных монет
        top_10_coins = sorted_coins[:10]

        response = "Список десяти самых волатильных криптовалют:\n"
        for coin in top_10_coins:
            name = coin["name"]
            price_change_percentage = coin["price_change_percentage_24h"]
            response += f"{name}: {price_change_percentage:.2f}%\n"

        update.message.reply_text(response)

if __name__ == "__main__":
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    # Обработчик команды для получения списка самых волатильных криптовалют
    dispatcher.add_handler(CommandHandler("topvolatility", send_top_volatility_coins))

    # Запускаем бота
    updater.start_polling()
    updater.idle()
