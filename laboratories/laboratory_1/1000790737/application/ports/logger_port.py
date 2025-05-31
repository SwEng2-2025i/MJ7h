import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from abc import ABCMeta, abstractmethod

from domain.entities.channel import NotificationChannel
from domain.entities.priority import Priority


class ILogger(metaclass=ABCMeta):
    @abstractmethod
    def info(self, message: str) -> None:
        """Log an informational message."""
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        """Log a warning message."""
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        """Log an error message."""
        pass

    @abstractmethod
    def send_attempt(
        self, to: str, channel: NotificationChannel, msg: str, priority: Priority
    ) -> None:
        """Log an attempt to send a notification via the specified channel."""
        pass

    @abstractmethod
    def send_success(
        self, to: str, channel: NotificationChannel, msg: str, priority: Priority
    ) -> None:
        """Log a successful notification send."""
        pass

    @abstractmethod
    def send_failure(
        self, to: str, channel: NotificationChannel, msg: str, priority: Priority
    ) -> None:
        """Log a failed notification send."""
        pass
