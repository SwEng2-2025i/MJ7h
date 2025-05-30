from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    username: str
    preferred_channel: str
    available_channels: List[str] = field(default_factory=list)