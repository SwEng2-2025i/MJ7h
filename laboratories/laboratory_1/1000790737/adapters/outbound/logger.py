import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from domain.entities.channel import NotificationChannel
from domain.entities.priority import Priority

from application.ports.logger_port import ILogger


class SimpleLogger(ILogger):
    """Simple logger implementation for demonstration purposes."""

    _instance = None

    @classmethod
    def get_instance(cls) -> "SimpleLogger":
        """Singleton instance of SimpleLogger."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def info(self, message: str) -> None:
        """Log an informational message."""
        print(f"[INFO] {message}")

    def warning(self, message: str) -> None:
        """Log a warning message."""
        print(f"[WARNING] {message}")

    def error(self, message: str) -> None:
        """Log an error message."""
        print(f"[ERROR] {message}")

    def send_attempt(
        self, to: str, channel: NotificationChannel, msg: str, priority: Priority
    ) -> None:
        """Log an attempt to send a notification via the specified channel."""
        print(
            f"[SEND ATTEMPT] To: {to}, Channel: {channel.value}, Message: {msg}, Priority: {priority.value}"
        )

    def send_success(
        self, to: str, channel: NotificationChannel, msg: str, priority: Priority
    ) -> None:
        """Log a successful notification send."""
        print(
            f"[SEND SUCCESS] To: {to}, Channel: {channel.value}, Message: {msg}, Priority: {priority.value}"
        )

    def send_failure(
        self, to: str, channel: NotificationChannel, msg: str, priority: Priority
    ) -> None:
        """Log a failed notification send."""
        print(
            f"[SEND FAILURE] To: {to}, Channel: {channel.value}, Message: {msg}, Priority: {priority.value}"
        )
