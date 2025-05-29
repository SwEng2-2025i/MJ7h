
from logger.logger import LoggerSingleton
from random import choice

class NotificationHandler():
    def __init__(self, next_handler=None):
        self.next_handler = next_handler
        self.logger = LoggerSingleton()

    def handle(self, user, notification):
        if self.next_handler:
            return self.next_handler.handle(user, notification)
        self.log(f"Notification could not be sent to {user.name}: {notification}")
        raise ConnectionError("No handler available to process the notification")

    def log(self, message):
        self.logger.log(message)

    def will_be_successful(self):
        return choice([True, False])
