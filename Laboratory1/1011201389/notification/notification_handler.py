
from logger.logger import LoggerSingleton
from random import choice

class NotificationHandler():

    # Base class for notification handlers
    def __init__(self, next_handler=None):
        self.next_handler = next_handler
        self.logger = LoggerSingleton() # Singleton logger instance

    # Handle the notification for a user
    def handle(self, user, notification):
        if self.next_handler:
            return self.next_handler.handle(user, notification)
        self._log(f"Notification could not be sent to {user.name} via any channel: {notification.message} (Priority: {notification.priority})")
        raise ConnectionError("No handler available to process the notification")

    # Log a message using the singleton logger, private method
    def _log(self, message):
        self.logger.log(message)

    # Check if the notification will be successful, simulating a random outcome
    def will_be_successful(self):
        return choice([True, False])
    
    # Property to get the channel name based on the handler class name
    @property
    def channel(self):
        return self.__class__.__name__.replace("Handler", "").lower()
    
    # Log success or failure of sending the notification
    def log_success(self, user, notification):
        self._log(f"Notification sent successfully to {user.name} via {self.channel}: {notification.message} (Priority: {notification.priority})")
    
    def log_failure(self, user, notification):
        self._log(f"Failed to send notification to {user.name} via {self.channel}: {notification.message} (Priority: {notification.priority})")
