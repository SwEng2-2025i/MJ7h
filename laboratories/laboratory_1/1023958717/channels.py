import random
from abc import ABC, abstractmethod
from logger import Logger
from models import Notification, User

class NotificationChannel(ABC):
    """
    Abstract base class for all notification channels.
    This acts as the Handler interface in the Chain of Responsibility pattern.
    """
    def __init__(self):
        self._next_handler: NotificationChannel = None
        self.logger = Logger.get_instance()

    def set_next(self, handler: 'NotificationChannel') -> 'NotificationChannel':
        """
        Sets the next handler in the chain.

        Args:
            handler (NotificationChannel): The next handler in the chain.

        Returns:
            NotificationChannel: The handler that was just set.
        """
        self._next_handler = handler
        return handler

    @abstractmethod
    def send(self, notification: Notification, user: User) -> bool:
        """
        Abstract method to send a notification. Concrete channels must implement this.
        If a channel fails, it should attempt to pass the notification to the next handler.

        Args:
            notification (Notification): The notification object to send.
            user (User): The user to whom the notification is being sent.

        Returns:
            bool: True if the notification was successfully sent by this channel or a subsequent one, False otherwise.
        """
        pass

class EmailChannel(NotificationChannel):
    """
    Concrete handler for sending notifications via email.
    Simulates success/failure and passes to the next handler on failure.
    """
    def __init__(self):
        super().__init__()
        self.channel_name = "email"

    def send(self, notification: Notification, user: User) -> bool:
        """
        Attempts to send the notification via email.
        """
        self.logger.log(f"Attempting to send '{notification.message}' to {user.name} via {self.channel_name}.")
        
        # Simulate random success/failure
        success = random.choice([True, False]) # 50% chance of failure

        if success:
            self.logger.log(f"Successfully sent '{notification.message}' to {user.name} via {self.channel_name}.")
            return True
        else:
            self.logger.log(f"Failed to send '{notification.message}' to {user.name} via {self.channel_name}. Retrying with next channel if available.")
            if self._next_handler:
                return self._next_handler.send(notification, user)
            else:
                self.logger.log(f"No more fallback channels for '{notification.message}' to {user.name}.")
                return False

class SMSChannel(NotificationChannel):
    """
    Concrete handler for sending notifications via SMS.
    Simulates success/failure and passes to the next handler on failure.
    """
    def __init__(self):
        super().__init__()
        self.channel_name = "sms"

    def send(self, notification: Notification, user: User) -> bool:
        """
        Attempts to send the notification via SMS.
        """
        self.logger.log(f"Attempting to send '{notification.message}' to {user.name} via {self.channel_name}.")

        # Simulate random success/failure
        success = random.choice([True, False]) # 50% chance of failure

        if success:
            self.logger.log(f"Successfully sent '{notification.message}' to {user.name} via {self.channel_name}.")
            return True
        else:
            self.logger.log(f"Failed to send '{notification.message}' to {user.name} via {self.channel_name}. Retrying with next channel if available.")
            if self._next_handler:
                return self._next_handler.send(notification, user)
            else:
                self.logger.log(f"No more fallback channels for '{notification.message}' to {user.name}.")
                return False

class ConsoleChannel(NotificationChannel):
    """
    Concrete handler for sending notifications to the console (as a last resort/backup).
    Simulates success/failure and passes to the next handler on failure (though typically this would be the end).
    """
    def __init__(self):
        super().__init__()
        self.channel_name = "console"

    def send(self, notification: Notification, user: User) -> bool:
        """
        Attempts to send the notification to the console.
        """
        self.logger.log(f"Attempting to send '{notification.message}' to {user.name} via {self.channel_name}.")

        self.logger.log(f"Successfully sent '{notification.message}' to {user.name} via {self.channel_name}. (Displayed on console)")
        print(f"CONSOLE NOTIFICATION for {user.name}: {notification.message}")
        return True


