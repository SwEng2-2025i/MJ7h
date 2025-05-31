from abc import ABC, abstractmethod
import random
from typing import Optional, List
from utils.logger import NotificationLogger

class NotificationChannel(ABC):
    def __init__(self):
        self.next_channel: Optional[NotificationChannel] = None
        self.logger = NotificationLogger()
    
    def set_next(self, channel: 'NotificationChannel') -> 'NotificationChannel':
        self.next_channel = channel
        return channel
    
    def notify(self, user: str, message: str, priority: str) -> bool:
        if self._send(user, message, priority):
            return True
        
        if self.next_channel:
            return self.next_channel.notify(user, message, priority)
        
        return False
    
    @abstractmethod
    def _send(self, user: str, message: str, priority: str) -> bool:
        pass

class EmailChannel(NotificationChannel):
    def _send(self, user: str, message: str, priority: str) -> bool:
        success = random.choice([True, False])
        if success:
            self.logger.info(f"Email sent to {user}: {message}")
        else:
            self.logger.warning(f"Failed to send email to {user}")
        return success

class SMSChannel(NotificationChannel):
    def _send(self, user: str, message: str, priority: str) -> bool:
        success = random.choice([True, False])
        if success:
            self.logger.info(f"SMS sent to {user}: {message}")
        else:
            self.logger.warning(f"Failed to send SMS to {user}")
        return success

class ConsoleChannel(NotificationChannel):
    def _send(self, user: str, message: str, priority: str) -> bool:
        success = True  # Console channel always succeeds
        self.logger.info(f"Console notification for {user}: {message}")
        return success

def create_channel_chain(channels: List[str]) -> Optional[NotificationChannel]:
    if not channels:
        return None
        
    channel_map = {
        'email': EmailChannel,
        'sms': SMSChannel,
        'console': ConsoleChannel
    }
    
    first_channel = None
    current_channel = None
    
    for channel_name in channels:
        channel_class = channel_map.get(channel_name)
        if channel_class:
            channel = channel_class()
            if not first_channel:
                first_channel = channel
            if current_channel:
                current_channel.set_next(channel)
            current_channel = channel
    
    return first_channel
