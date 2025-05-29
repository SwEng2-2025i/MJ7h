
from logger.logger import LoggerSingleton
from random import choice

class NotificationHandler():
    def __init__(self, next_handler=None):
        self.next_handler = next_handler
        self.logger = LoggerSingleton()

    def handle(self, user, notification):
        if self.next_handler:
            return self.next_handler.handle(user, notification)
        self.log(f"Notification could not be sent to {user.name} vian any channel: {notification.message} (Priority: {notification.priority})")
        raise ConnectionError("No handler available to process the notification")

    def log(self, message):
        self.logger.log(message)

    def will_be_successful(self):
        return choice([True, False])
    
    @property
    def channel(self):
        return self.__class__.__name__.replace("Handler", "").lower()
    
    def log_success(self, user, notification):
        self.log(f"Notification sent successfully to {user.name} via {self.channel}: {notification.message} (Priority: {notification.priority})")
    
    def log_failure(self, user, notification):
        self.log(f"Failed to send notification to {user.name} via {self.channel}: {notification.message} (Priority: {notification.priority})")
