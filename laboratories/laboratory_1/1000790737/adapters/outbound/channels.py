import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from domain.entities.channel import NotificationChannel

from application.services.strategy import SendStrategy
from application.services.user_service import UserService


class SmsSender(SendStrategy):
    """Concrete implementation of SendStrategy for sending SMS messages."""

    def __init__(self, strategy: SendStrategy, user_service: UserService) -> None:
        self.strategy = strategy
        self.user_service = user_service

    @property
    def channel(self) -> NotificationChannel:
        """Return the channel used by this strategy."""
        return NotificationChannel.SMS

    def send(self, to: str, message: str) -> bool:
        """Send an SMS message using the specified strategy."""
        if not self.user_service.is_user_registered(to):
            raise ValueError(f"User {to} is not registered.")

        user = self.user_service.get_user(to)
        if not user:
            raise ValueError(f"User {to} not found.")
        if self.channel not in user.available_channels:
            raise ValueError(
                f"User {to} does not have the {self.channel.value} channel available."
            )

        return self.strategy.send_msg(user, message, self.channel)


class EmailSender(SendStrategy):
    """Concrete implementation of SendStrategy for sending email messages."""

    def __init__(self, strategy: SendStrategy, user_service: UserService) -> None:
        self.strategy = strategy
        self.user_service = user_service

    @property
    def channel(self) -> NotificationChannel:
        """Return the channel used by this strategy."""
        return NotificationChannel.EMAIL

    def send(self, to: str, message: str) -> bool:
        """Send an email message using the specified strategy."""
        if not self.user_service.is_user_registered(to):
            raise ValueError(f"User {to} is not registered.")

        user = self.user_service.get_user(to)
        if not user:
            raise ValueError(f"User {to} not found.")
        if self.channel not in user.available_channels:
            raise ValueError(
                f"User {to} does not have the {self.channel.value} channel available."
            )

        return self.strategy.send_msg(user, message, self.channel)


class AppNotificationSender(SendStrategy):
    """Concrete implementation of SendStrategy for sending app notifications."""

    def __init__(self, strategy: SendStrategy, user_service: UserService) -> None:
        self.strategy = strategy
        self.user_service = user_service

    @property
    def channel(self) -> NotificationChannel:
        """Return the channel used by this strategy."""
        return NotificationChannel.APP_NOTIFICATION

    def send(self, to: str, message: str) -> bool:
        """Send an app notification using the specified strategy."""
        if not self.user_service.is_user_registered(to):
            raise ValueError(f"User {to} is not registered.")

        user = self.user_service.get_user(to)
        if not user:
            raise ValueError(f"User {to} not found.")
        if self.channel not in user.available_channels:
            raise ValueError(
                f"User {to} does not have the {self.channel.value} channel available."
            )

        return self.strategy.send_msg(user, message, self.channel)


class SmokeSignalSender(SendStrategy):
    """Concrete implementation of SendStrategy for sending smoke signals."""

    def __init__(self, strategy: SendStrategy, user_service: UserService) -> None:
        self.strategy = strategy
        self.user_service = user_service

    @property
    def channel(self) -> NotificationChannel:
        """Return the channel used by this strategy."""
        return NotificationChannel.SMOKE_SIGNAL

    def send(self, to: str, message: str) -> bool:
        """Send a smoke signal using the specified strategy."""
        if not self.user_service.is_user_registered(to):
            raise ValueError(f"User {to} is not registered.")

        user = self.user_service.get_user(to)
        if not user:
            raise ValueError(f"User {to} not found.")
        if self.channel not in user.available_channels:
            raise ValueError(
                f"User {to} does not have the {self.channel.value} channel available."
            )

        return self.strategy.send_msg(user, message, self.channel)


class CarrierPigeonSender(SendStrategy):
    """Concrete implementation of SendStrategy for sending messages via carrier pigeon."""

    def __init__(self, strategy: SendStrategy, user_service: UserService) -> None:
        self.strategy = strategy
        self.user_service = user_service

    @property
    def channel(self) -> NotificationChannel:
        """Return the channel used by this strategy."""
        return NotificationChannel.IP_O_AC

    def send(self, to: str, message: str) -> bool:
        """Send a message using a carrier pigeon."""
        if not self.user_service.is_user_registered(to):
            raise ValueError(f"User {to} is not registered.")

        user = self.user_service.get_user(to)
        if not user:
            raise ValueError(f"User {to} not found.")
        if self.channel not in user.available_channels:
            raise ValueError(
                f"User {to} does not have the {self.channel.value} channel available."
            )

        return self.strategy.send_msg(user, message, self.channel)


class UnknownChannelSender(SendStrategy):
    """Concrete implementation of SendStrategy for sending messages via unknown channels."""

    def __init__(self, strategy: SendStrategy, user_service: UserService) -> None:
        self.strategy = strategy
        self.user_service = user_service

    @property
    def channel(self) -> NotificationChannel:
        """Return the channel used by this strategy."""
        return NotificationChannel.UNKNOWN

    def send(self, to: str, message: str) -> bool:
        """Send a message using an unknown channel."""
        raise ValueError(
            f"Unknown channel {self.channel.value} cannot be used to send messages."
        )
