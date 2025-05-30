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
            self.available_channels.insert(0, preferred_channel)

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
        return self._available_channels
