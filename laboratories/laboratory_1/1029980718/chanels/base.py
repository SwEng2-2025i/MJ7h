import random
from logger.logger import Logger

class NotificationHandler:
    def __init__(self):
        self.next_handler = None
    
    def set_next(self, handler):
        self.next_handler = handler
        return handler
    
    def handle(self, user, message):
        raise NotImplementedError("Must implement in subclass")

    def attempt(self, channel_name, user_name, message):
        Logger().log(f"Attempting {channel_name} for {user_name}")
        success = random.choice([True, False])
        Logger().log(f"{channel_name} {'Success' if success else 'Failure'}")
        return success
