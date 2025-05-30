from abc import ABCMeta, abstractmethod
from ..entities.user import User


class INotificationSender(metaclass=ABCMeta):
    @abstractmethod
    def send(self, to: User, message: str) -> None:
        """Send a notification with the given message."""
        pass
