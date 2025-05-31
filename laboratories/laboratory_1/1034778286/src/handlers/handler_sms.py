from src.utils.logger import logger
from src.handlers.handler import Handler
import random

class SMSHandler(Handler):

    def handle(self, data):
        success = random.choice([True, False])
        if success:
            logger.info("Notification successfully sent via SMS: %s", data)
        else:
            logger.warning("Notification failed via Email, trying next channel: %s", data)
        super().handle(data)