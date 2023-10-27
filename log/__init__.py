from .loggHandler import *

def init(level):
    
    logging.basicConfig(level=level, filename="log/log.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding='utf-8')

    # Отключаем логирование с уровнем DEBUG для модуля urllib3.connectionpool
    urllib3_logger = logging.getLogger('urllib3.connectionpool')
    urllib3_logger.setLevel(logging.WARNING)

    # Отключаем логирование с уровнем DEBUG для модуля aiogram
    aiogram_logger = logging.getLogger('aiogram')
    aiogram_logger.setLevel(logging.WARNING)
