import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from domain.entities.channel import NotificationChannel
from typing import List


class User:
    def __init__(
        self,
        user_name: str,
        preferred_channel: NotificationChannel,
        available_channels: List[NotificationChannel],
    ):
        self._user_name = user_name
        self._preferred_channel = preferred_channel
        self._available_channels = available_channels

        if preferred_channel not in available_channels:
            self.available_channels.insert(0, preferred_channel)

    # For this example, the
    @property
    def user_name(self) -> str:
        return self._user_name

    @property
    def preferred_channel(self) -> NotificationChannel:
        return self._preferred_channel

    @property
    def available_channels(self) -> List[NotificationChannel]:
        return self._available_channels
