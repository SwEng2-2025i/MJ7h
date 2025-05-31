from channels.base_channel import BaseChannel
from utils.logger import Logger
import random

class SmsChannel(BaseChannel):
    def handle(self, preferred, message):
        logger = Logger.get_instance()
        logger.log("Trying sms channel...")
        success = random.choice([True, False])
        if preferred == "sms" or not preferred:
            if success:
                return {"status": "success", "channel": "sms"}
        return self.try_next(preferred, message)