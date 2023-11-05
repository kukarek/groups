import logging
from vk_api.vk_api import VkApiMethod
from database import sql
from misc.config import API_TOKEN
from aiogram import Bot
import asyncio

class ERROR(logging.Handler):
    """
    Обработчик error логов
    """
    def __init__(self, level = 0, vk: VkApiMethod = None, group_id = None) -> None:
        super().__init__(level)
        self.vk = vk
        self.group_id = group_id

    def emit(self, record: logging.LogRecord) -> None:
        """
        отправка сообщения с ошибкой админу
        """
        try:
            if record.levelno == logging.ERROR:
                admins = sql.get_vk_admins(self.group_id)
                for admin in admins:
                    self.vk.messages.send(user_id=admin, message=f"Ошибка: {record.msg}", random_id = 0)
        except Exception as e:
            logging.critical(f"Ошибка отправки вк уведомления об ошибке) {e}")

