from misc import ADMINS
import asyncio
from vk_bot.bot.main import vk
import logging


class ERROR(logging.Handler):
    """
    Обработчик error логов
    """
    def emit(self, record: logging.LogRecord) -> None:
        """
        отправка сообщения с ошибкой админу
        """
        if record.levelno == logging.ERROR:
            for admin in ADMINS:
                vk.messages.send(user_id=admin, message=f"Ошибка: {record.msg}", random_id = 0)

