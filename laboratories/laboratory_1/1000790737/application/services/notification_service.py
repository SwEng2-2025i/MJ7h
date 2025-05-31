import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from domain.ports.user_repository import IUserRepository
from domain.entities.priority import Priority

from application.exceptions import (
    UserNotFoundException,
    NotificationChainFailedException,
)
from application.ports.logger_port import ILogger
from application.services.chain import ChainSender


class NotificationService:
    def __init__(
        self,
        sender_chain: ChainSender,
        user_repository: IUserRepository,
        logger: ILogger,
    ):
        self.sender_chain = sender_chain
        self.user_repository = user_repository
        self.logger = logger

    @property
    def sender_chain(self) -> ChainSender:
        """Return the sender chain used by this service."""
        return self._sender_chain

    @sender_chain.setter
    def sender_chain(self, value: ChainSender) -> None:
        """Set the sender chain used by this service."""
        self._sender_chain = value

    def send_notification(
        self, user_name: str, message: str, priority: str
    ) -> dict[str, str]:
        """Send a notification to the user with the given user_name."""
        user = self.user_repository.get(user_name)
        msg_priority = Priority(priority.lower())
        if not user:
            raise UserNotFoundException(f"User {user_name} not found.")
        if not user.available_channels:
            raise UserNotFoundException(f"User {user_name} has no available channels.")

        try:
            channel = self.sender_chain.send(user, message, msg_priority)
            return {
                "status": "success",
                "user_name": user_name,
                "channel": channel.value,
                "message": message,
                "priority": msg_priority.value,
            }
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")

        self.logger.warning(
            f"Notification chain failed for user {user_name} with message: {message}"
        )
        raise NotificationChainFailedException(
            f"Failed to send notification to {user_name} using all available channels."
        )
