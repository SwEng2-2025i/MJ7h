from channels.base_channel import BaseChannel
from utils.logger import Logger
import random

class ConsoleChannel(BaseChannel):
    def handle(self, preferred, message):
        logger = Logger.get_instance()
        logger.log("Trying console channel...")
        success = random.choice([True, False])
        if preferred == "console" or not preferred:
            if success:
                return {"status": "success", "channel": "console"}
        return self.try_next(preferred, message)
