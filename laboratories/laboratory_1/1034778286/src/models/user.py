from dataclasses import dataclass
from typing import List

@dataclass
class User:
    name: str
    preferred_channel: str
    available_channels: List[str]