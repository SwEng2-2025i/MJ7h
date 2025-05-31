import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from typing import List

from domain.ports.notification_sender import INotificationSender
from domain.entities.priority import Priority
from domain.entities.user import User
from domain.entities.channel import NotificationChannel

from application.exceptions import NotificationChainFailedException


class ChainSender:
    """Chain of responsibility for sending notifications."""

    def __init__(
        self,
        available_senders: List[INotificationSender],
    ):
        self.senders_dict = {s.channel: s for s in available_senders}

    def send(self, user: User, message: str, priority: Priority) -> NotificationChannel:
        """Send a notification to the user using the chain of responsibility."""
        if not user.available_channels:
            raise NotificationChainFailedException(
                f"User {user.user_name} has no available channels."
            )

        first_channel = user.available_channels[0]
        if first_channel not in self.senders_dict:
            raise NotificationChainFailedException(
                f"Channel {first_channel} is not available for sending notifications."
            )

        for channel in user.available_channels:
            sender = self.senders_dict.get(channel)
            if not sender:
                continue

            success = sender.send(user.user_name, message, priority.value)

            if success:
                return channel

        raise NotificationChainFailedException(
            f"Failed to send notification to {user.user_name} using all available channels."
        )
