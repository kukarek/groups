import logging
from aiogram import Bot, Dispatcher, executor
import tg_bot
from misc.config import API_TOKEN

logg = logging.getLogger(__name__)
bot = Bot(token=API_TOKEN["helper"])

async def on_start(dp: Dispatcher):
      
    tg_bot.bot.register_all_handlers(dp)
    logg.debug("Все модули зарегестрированы!")


def start_bot():

    dp = Dispatcher(bot)
    # Запуск бота
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)

if __name__ == '__main__':
    start_bot()
    
