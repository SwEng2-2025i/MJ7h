from abc import ABC, abstractmethod
from utils.logger import logger
import random

class NotificationHandler(ABC):
    def __init__(self, next_handler=None):
        self._next_handler = next_handler

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, user, message, priority):
        if self.can_handle(user):
            if self.send_notification(user, message, priority):
                logger.log(f"Notification sent via {self.__class__.__name__} to {user['name']}.")
                return True
            else:
                logger.log(f"Failed to send notification via {self.__class__.__name__} to {user['name']}. Trying next...")
        
        if self._next_handler:
            return self._next_handler.handle(user, message, priority)
        
        logger.log(f"All notification channels failed for user {user['name']}.")
        return False

    @abstractmethod
    def can_handle(self, user):
        pass

    @abstractmethod
    def send_notification(self, user, message, priority):
        # Simulate random failure
        return random.choice([True, False]) 