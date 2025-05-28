from app.channels.base_channel import NotificationChannel
from app.utils.logger import Logger
import random

class EmailChannel(NotificationChannel):
    def send(self, message):
        logger = Logger()
        success = random.choice([True, False])
        logger.log("email", message, "success" if success else "fail")

        if success:
            return True
        elif self.next_channel:
            return self.next_channel.send(message)
        return False

