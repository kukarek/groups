from misc import ADMINS
import logging
from vk_api.vk_api import VkApiMethod


class ERROR(logging.Handler):
    """
    Обработчик error логов
    """
    def __init__(self, level = 0, vk: VkApiMethod = None) -> None:
        super().__init__(level)
        self.vk = vk

    def emit(self, record: logging.LogRecord) -> None:
        """
        отправка сообщения с ошибкой админу
        """
        try:
            if record.levelno == logging.ERROR:
                for admin in ADMINS:
                    self.vk.messages.send(user_id=admin, message=f"Ошибка из {record.name}:  {record.msg}", random_id = 0)
        except:
            logging.critical("Ошибка отправки уведомления об ошибке)")

