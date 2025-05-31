import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from domain.entities.channel import NotificationChannel
from typing import List, Optional


class User:
    def __init__(
        self,
        user_name: str,
        preferred_channel: NotificationChannel,
        available_channels: List[NotificationChannel],
        phone_number: Optional[str] = None,
        email: Optional[str] = None,
    ):
        self._user_name = user_name
        self._preferred_channel = preferred_channel
        self._available_channels = available_channels

        self._phone_number = phone_number
        self._email = email

        if preferred_channel not in available_channels:
            self._available_channels.insert(0, preferred_channel)

    def __repr__(self) -> str:
        return (
            f"User(user_name={self._user_name}, "
            f"preferred_channel={self._preferred_channel}, "
            f"available_channels={self._available_channels}, "
            f"phone_number={self._phone_number}, "
            f"email={self._email})"
        )

    # For this example, the
    @property
    def user_name(self) -> str:
        return self._user_name

    @property
    def phone_number(self) -> Optional[str]:
        return self._phone_number

    @property
    def email(self) -> Optional[str]:
        return self._email

    @property
    def preferred_channel(self) -> NotificationChannel:
        return self._preferred_channel

    @property
    def available_channels(self) -> List[NotificationChannel]:
        if self._available_channels[0] != self._preferred_channel:
            ordered_channels = [self._preferred_channel]
            ordered_channels.extend(
                channel
                for channel in self._available_channels
                if channel != self._preferred_channel
            )

        return self._available_channels
