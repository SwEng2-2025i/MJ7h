import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from domain.ports.user_repository import IUserRepository

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

    def send_notification(self, user_name: str, message: str) -> dict[str, str]:
        """Send a notification to the user with the given user_name."""
        user = self.user_repository.get(user_name)
        if not user:
            raise UserNotFoundException(f"User {user_name} not found.")

        for channel in user.available_channels:
            self.logger.send_attempt(user_name, channel, message)
            try:
                self.logger.send_attempt(user_name, channel, message)
                sent_channel = self.sender_chain.send(user, message)
                self.logger.send_success(user_name, sent_channel, message)
                return {
                    "status": "success",
                    "user_name": user_name,
                    "channel": sent_channel.value,
                    "message": message,
                }
            except Exception as e:
                self.logger.send_failure(user_name, channel, message)
                self.logger.error(f"Failed to send notification: {e}")

        raise NotificationChainFailedException(
            f"User {user_name} not found or no available channels."
        )
