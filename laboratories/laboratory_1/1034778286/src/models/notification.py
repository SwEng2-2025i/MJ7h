from dataclasses import dataclass
from typing import List
from src.models.user import User

@dataclass
class Notification:
    user: str
    message: str
    priority: str
