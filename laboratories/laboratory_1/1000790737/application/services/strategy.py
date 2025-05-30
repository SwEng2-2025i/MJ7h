import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import random
from abc import ABCMeta, abstractmethod

from domain.entities.user import User
from domain.entities.channel import NotificationChannel

from application.ports.logger_port import ILogger


class SendStrategy(metaclass=ABCMeta):
    """Abstract base class for sending messages.

    IMPORTANT: It may seem that the algorithms are the same. For the scope of this lab no
    complex logic is performed, but in a real scenario this strategy allows to modify the
    sending algorithm in a much simpler way and even implement multiple providers, for
    example using Twilio and Textmagic.
    """

    @abstractmethod
    def send_msg(self, to: User, message: str) -> bool:
        """Send an SMS to the specified phone number with the given message."""
        pass


class SmsStrategy(SendStrategy):
    """Concrete strategy for sending SMS messages."""

    def __init__(self, logger: ILogger) -> None:
        self.logger = logger

    def _send_sms(self, phone_number: str, message: str) -> bool:
        # Simulate sending an SMS using an invented company
        is_success = random.randint(0, 1) == 1
        self.logger.send_attempt(
            to=phone_number,
            channel=NotificationChannel.SMS,
            msg=message,
        )

        if is_success:
            self.logger.send_success(
                to=phone_number, channel=NotificationChannel.SMS, msg=message
            )
        else:
            self.logger.send_failure(
                to=phone_number, channel=NotificationChannel.SMS, msg=message
            )

        return is_success

    def send_msg(self, to: User, message: str) -> bool:
        """Send an SMS to the specified user with the given message."""
        if not to.phone_number:
            self.logger.send_failure(
                to="Non-Existing Number", channel=NotificationChannel.SMS, msg=message
            )
            return False

        return self._send_sms(to.phone_number, message)


class EmailStrategy(SendStrategy):
    """Concrete strategy for sending email messages."""

    def __init__(self, logger: ILogger) -> None:
        self.logger = logger

    def _send_email(self, email: str, message: str) -> bool:
        # Simulate sending an email using an invented company
        is_success = random.choice([True, False])
        self.logger.send_attempt(
            to=email,
            channel=NotificationChannel.EMAIL,
            msg=message,
        )

        if is_success:
            self.logger.send_success(
                to=email, channel=NotificationChannel.EMAIL, msg=message
            )
        else:
            self.logger.send_failure(
                to=email, channel=NotificationChannel.EMAIL, msg=message
            )

        return is_success

    def send_msg(self, to: User, message: str) -> bool:
        """Send an email to the specified user with the given message."""
        if not to.email:
            self.logger.send_failure(
                to="Non-Existing Email", channel=NotificationChannel.EMAIL, msg=message
            )
            return False

        return self._send_email(to.email, message)


class PushStrategy(SendStrategy):
    """Concrete strategy for sending push notifications."""

    def __init__(self, logger: ILogger) -> None:
        self.logger = logger

    def _send_push(self, user_name: str, message: str) -> bool:
        # Simulate sending a push notification using an invented company
        is_success = random.randint(0, 1) == 1
        self.logger.send_attempt(
            to=user_name,
            channel=NotificationChannel.APP_NOTIFICATION,
            msg=message,
        )

        if is_success:
            self.logger.send_success(
                to=user_name, channel=NotificationChannel.APP_NOTIFICATION, msg=message
            )
        else:
            self.logger.send_failure(
                to=user_name, channel=NotificationChannel.APP_NOTIFICATION, msg=message
            )

        return is_success

    def send_msg(self, to: User, message: str) -> bool:
        """Send a push notification to the specified user with the given message."""
        return self._send_push(to.user_name, message)


class SmokeSignalStrategy(SendStrategy):
    """Concrete strategy for sending smoke signals."""

    def __init__(self, logger: ILogger) -> None:
        self.logger = logger

    def _send_smoke_signal(self, user_name: str, message: str) -> bool:
        # Simulate sending a smoke signal using an invented company
        is_success = random.choice([True, False])
        self.logger.send_attempt(
            to=user_name,
            channel=NotificationChannel.SMOKE_SIGNAL,
            msg=message,
        )

        if is_success:
            self.logger.send_success(
                to=user_name, channel=NotificationChannel.SMOKE_SIGNAL, msg=message
            )
        else:
            self.logger.send_failure(
                to=user_name, channel=NotificationChannel.SMOKE_SIGNAL, msg=message
            )

        return is_success

    def send_msg(self, to: User, message: str) -> bool:
        """Send a smoke signal to the specified user with the given message."""
        return self._send_smoke_signal(to.user_name, message)


class IpoacStrategy(SendStrategy):
    """Concrete strategy for sending IP Over Avian Carriers messages."""

    def __init__(self, logger: ILogger) -> None:
        self.logger = logger

    def _send_ipoac(self, user_name: str, message: str) -> bool:
        # Simulate sending an IP Over Avian Carriers message using an invented company
        is_success = random.choice([True, False])
        self.logger.send_attempt(
            to=user_name,
            channel=NotificationChannel.IP_O_AC,
            msg=message,
        )

        if is_success:
            self.logger.send_success(
                to=user_name, channel=NotificationChannel.IP_O_AC, msg=message
            )
        else:
            self.logger.send_failure(
                to=user_name, channel=NotificationChannel.IP_O_AC, msg=message
            )

        return is_success

    def send_msg(self, to: User, message: str) -> bool:
        """Send an IP Over Avian Carriers message to the specified user with the given message."""
        return self._send_ipoac(to.user_name, message)


class UnknownStrategy(SendStrategy):
    """Concrete strategy for handling unknown channels."""

    def __init__(self, logger: ILogger) -> None:
        self.logger = logger

    def send_msg(self, to: User, message: str) -> bool:
        """Handle unknown channel by logging an error."""
        self.logger.send_failure(
            to=to.user_name,
            channel=NotificationChannel.UNKNOWN,
            msg=message,
        )
        return False
