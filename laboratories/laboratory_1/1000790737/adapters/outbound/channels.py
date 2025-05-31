import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from domain.entities.channel import NotificationChannel
from domain.ports.notification_sender import INotificationSender
from domain.entities.priority import Priority

from application.services.strategy import SendStrategy
from application.services.user_service import UserService


class SmsSender(INotificationSender):
    """Concrete implementation of SendStrategy for sending SMS messages."""

    def __init__(self, strategy: SendStrategy, user_service: UserService) -> None:
        self.strategy = strategy
        self.user_service = user_service

        self.next = None

    def set_next(self, next_handler: "INotificationSender") -> "INotificationSender":
        """Set the next handler in the chain."""
        self.next = next_handler
        return next_handler

    @property
    def channel(self) -> NotificationChannel:
        """Return the channel used by this strategy."""
        return NotificationChannel.SMS

    def send(self, to: str, message: str, priority: str) -> bool:
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

        return self.strategy.send_msg(
            user, message, self.channel, priority=Priority(priority)
        )


class EmailSender(INotificationSender):
    """Concrete implementation of SendStrategy for sending email messages."""

    def __init__(self, strategy: SendStrategy, user_service: UserService) -> None:
        self.strategy = strategy
        self.user_service = user_service

        self.next = None

    def set_next(self, next_handler: "INotificationSender") -> "INotificationSender":
        """Set the next handler in the chain."""
        self.next = next_handler
        return next_handler

    @property
    def channel(self) -> NotificationChannel:
        """Return the channel used by this strategy."""
        return NotificationChannel.EMAIL

    def send(self, to: str, message: str, priority: str) -> bool:
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

        return self.strategy.send_msg(
            user, message, self.channel, priority=Priority(priority)
        )


class AppNotificationSender(INotificationSender):
    """Concrete implementation of SendStrategy for sending app notifications."""

    def __init__(self, strategy: SendStrategy, user_service: UserService) -> None:
        self.strategy = strategy
        self.user_service = user_service

        self.next = None

    def set_next(self, next_handler: "INotificationSender") -> "INotificationSender":
        """Set the next handler in the chain."""
        self.next = next_handler
        return next_handler

    @property
    def channel(self) -> NotificationChannel:
        """Return the channel used by this strategy."""
        return NotificationChannel.APP_NOTIFICATION

    def send(self, to: str, message: str, priority: str) -> bool:
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

        return self.strategy.send_msg(
            user, message, self.channel, priority=Priority(priority)
        )


class SmokeSignalSender(INotificationSender):
    """Concrete implementation of SendStrategy for sending smoke signals."""

    def __init__(self, strategy: SendStrategy, user_service: UserService) -> None:
        self.strategy = strategy
        self.user_service = user_service

        self.next = None

    def set_next(self, next_handler: "INotificationSender") -> "INotificationSender":
        """Set the next handler in the chain."""
        self.next = next_handler
        return next_handler

    @property
    def channel(self) -> NotificationChannel:
        """Return the channel used by this strategy."""
        return NotificationChannel.SMOKE_SIGNAL

    def send(self, to: str, message: str, priority: str) -> bool:
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

        return self.strategy.send_msg(
            user, message, self.channel, priority=Priority(priority)
        )


class CarrierPigeonSender(INotificationSender):
    """Concrete implementation of SendStrategy for sending messages via carrier pigeon."""

    def __init__(self, strategy: SendStrategy, user_service: UserService) -> None:
        self.strategy = strategy
        self.user_service = user_service

        self.next = None

    def set_next(self, next_handler: "INotificationSender") -> "INotificationSender":
        """Set the next handler in the chain."""
        self.next = next_handler
        return next_handler

    @property
    def channel(self) -> NotificationChannel:
        """Return the channel used by this strategy."""
        return NotificationChannel.IP_O_AC

    def send(self, to: str, message: str, priority: str) -> bool:
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

        return self.strategy.send_msg(
            user, message, self.channel, priority=Priority(priority)
        )


class UnknownChannelSender(INotificationSender):
    """Concrete implementation of SendStrategy for sending messages via unknown channels."""

    def __init__(self, strategy: SendStrategy, user_service: UserService) -> None:
        self.strategy = strategy
        self.user_service = user_service

    @property
    def channel(self) -> NotificationChannel:
        """Return the channel used by this strategy."""
        return NotificationChannel.UNKNOWN

    def send(self, to: str, message: str, priority: str) -> bool:
        """Send a message using an unknown channel."""
        raise ValueError(
            f"Unknown channel {self.channel.value} cannot be used to send messages."
        )
