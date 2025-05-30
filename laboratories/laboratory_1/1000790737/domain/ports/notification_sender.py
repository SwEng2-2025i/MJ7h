import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from abc import ABCMeta, abstractmethod

from domain.entities.user import User
from domain.entities.channel import NotificationChannel


class INotificationSender(metaclass=ABCMeta):
    """Interface for sending notifications to users. (Chain of Responsibility Pattern - Handler)"""

    @abstractmethod
    def set_next(self, next_handler: "INotificationSender") -> "INotificationSender":
        """Set the next handler in the chain."""
        pass

    @abstractmethod
    def send(self, to: User, message: str) -> NotificationChannel:
        """Send a notification with the given message."""
        pass

    @property
    @abstractmethod
    def channel(self) -> NotificationChannel:
        """Return the channel used for sending notifications."""
        pass
