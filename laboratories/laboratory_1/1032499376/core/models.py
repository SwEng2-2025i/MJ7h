# core/models.py
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional
import uuid
import datetime as dt


class ChannelType(Enum):
    EMAIL = auto()
    SMS = auto()
    CONSOLE = auto()


@dataclass
class User:
    id: str
    name: str
    preferred_channel: ChannelType
    backup_channels: List[ChannelType] = field(default_factory=list)

    @staticmethod
    def create(name: str,
               preferred: ChannelType,
               backups: Optional[List[ChannelType]] = None) -> "User":
        return User(
            id=str(uuid.uuid4()),
            name=name,
            preferred_channel=preferred,
            backup_channels=backups or []
        )


@dataclass
class Notification:
    id: str
    user: User
    message: str
    created_at: dt.datetime = field(
        default_factory=lambda: dt.datetime.now(dt.timezone.utc)  # timezone-aware
    )

    @staticmethod
    def create(user: User, message: str) -> "Notification":
        return Notification(id=str(uuid.uuid4()), user=user, message=message)
