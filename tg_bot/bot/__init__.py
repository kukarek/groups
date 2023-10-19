from .handlers import *
from aiogram import Dispatcher

def register_all_handlers(dp: Dispatcher):

    dp.register_message_handler(on_start, commands=['start'])
    dp.register_message_handler(get_top, commands=['get_top'])
    dp.register_message_handler(on_help, commands=['help'])
    dp.register_message_handler(balance, commands=['balance'])
    dp.register_message_handler(status, commands=['status'])
    dp.register_message_handler(echo)

                                

