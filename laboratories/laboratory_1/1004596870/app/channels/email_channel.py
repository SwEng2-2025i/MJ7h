from channels.base_channel import BaseChannel
from utils.logger import Logger
import random

class EmailChannel(BaseChannel):
    def handle(self, preferred, message):
        logger = Logger.get_instance()
        logger.log("Trying email channel...")
        success = random.choice([True, False])
        if preferred == "email" or not preferred:
            if success:
                return {"status": "success", "channel": "email"}
        return self.try_next(preferred, message)
