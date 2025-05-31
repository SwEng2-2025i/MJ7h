from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogEntry:
    timestamp: str
    username: str
    channel: str
    message: str
    priority: str
    successful: bool  # "Successful" or "Failed"