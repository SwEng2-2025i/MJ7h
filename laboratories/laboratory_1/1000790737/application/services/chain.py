import sys, os

from ...domain.entities.user import User

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from typing import List

from domain.ports.notification_sender import INotificationSender
from domain.entities.channel import NotificationChannel

from application.ports.logger_port import ILogger
from application.exceptions import NotificationChainFailedException


class ChainSender(INotificationSender):
    """Chain of responsibility for sending notifications."""

    def __init__(self, senders: List[INotificationSender], logger: ILogger):
        self.senders = senders
        self.logger = logger

    def send(self, to: User, message: str) -> NotificationChannel:
        for sender in self.senders:
            channel = sender.channel
            self.logger.send_attempt(to.user_name, channel, message)

            if sender.send(to, message):
                self.logger.send_success(to.user_name, channel, message)
                return channel
            self.logger.send_failure(to.user_name, channel, message)

        raise NotificationChainFailedException(
            f"Failed to send notification to {to.user_name} via all available channels."
        )
