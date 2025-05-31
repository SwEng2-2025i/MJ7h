import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import random
from abc import ABCMeta, abstractmethod

from domain.entities.user import User
from domain.entities.channel import NotificationChannel
from domain.entities.priority import Priority

from application.ports.logger_port import ILogger


class SendStrategy(metaclass=ABCMeta):
    """Abstract base class for sending messages.

    IMPORTANT: It may seem that the algorithms are the same. For the scope of this lab no
    complex logic is performed, but in a real scenario this strategy allows to modify the
    sending algorithm in a much simpler way and even implement multiple providers, for
    example using Twilio and Textmagic.
    """

    @abstractmethod
    def send_msg(
        self, to: User, message: str, channel: NotificationChannel, priority: Priority
    ) -> bool:
        """Send an SMS to the specified phone number with the given message."""
        pass


class RandomChoiceStrategy(SendStrategy):
    """Concrete strategy for randomly choosing a channel to send messages."""

    def __init__(self, logger: ILogger) -> None:
        self.logger = logger

    def send_msg(
        self, to: User, message: str, channel: NotificationChannel, priority: Priority
    ) -> bool:
        """Randomly choose a strategy to send the message."""
        # Simulate sending an IP Over Avian Carriers message using an invented company
        is_success = random.choice([True, False])
        self.logger.send_attempt(
            to=to.user_name,
            channel=channel,
            msg=message,
            priority=priority,
        )

        if is_success:
            self.logger.send_success(
                to=to.user_name, channel=channel, msg=message, priority=priority
            )
        else:
            self.logger.send_failure(
                to=to.user_name, channel=channel, msg=message, priority=priority
            )
        return is_success


class RandomIntStrategy(SendStrategy):
    """Concrete strategy for randomly choosing a channel to send messages."""

    def __init__(self, logger: ILogger) -> None:
        self.logger = logger

    def send_msg(
        self, to: User, message: str, channel: NotificationChannel, priority: Priority
    ) -> bool:
        """Randomly choose a strategy to send the message."""
        # Simulate sending an IP Over Avian Carriers message using an invented company
        is_success = random.randint(0, 1) == 1
        self.logger.send_attempt(
            to=to.user_name,
            channel=channel,
            msg=message,
            priority=priority,
        )

        if is_success:
            self.logger.send_success(
                to=to.user_name, channel=channel, msg=message, priority=priority
            )
        else:
            self.logger.send_failure(
                to=to.user_name, channel=channel, msg=message, priority=priority
            )
        return is_success
