"""
Notification model for the notification system
"""

from typing import Optional
from datetime import datetime
import uuid

class Notification:
    """
    Represents a notification in the system
    """
    
    def __init__(self, user_name: str, message: str, priority: str):
        """
        Initialize a new notification
        
        Args:
            user_name: Target user's name
            message: Notification message
            priority: Notification priority (high, medium, low)
        """
        self.id = str(uuid.uuid4())
        self.user_name = user_name
        self.message = message
        self.priority = priority
        self.created_at = datetime.now()
        self.delivered = False
        self.delivery_channel: Optional[str] = None
        self.attempts = 0
    
    def mark_delivered(self, channel: str):
        """
        Mark notification as delivered
        
        Args:
            channel: The channel through which the notification was delivered
        """
        self.delivered = True
        self.delivery_channel = channel
    
    def add_attempt(self):
        """
        Increment the number of delivery attempts
        """
        self.attempts += 1
    
    def to_dict(self) -> dict:
        """
        Convert notification object to dictionary
        
        Returns:
            Dictionary representation of the notification
        """
        return {
            'id': self.id,
            'user_name': self.user_name,
            'message': self.message,
            'priority': self.priority,
            'timestamp': self.created_at.isoformat(),
            'created_at': self.created_at.isoformat(),
            'delivered': self.delivered,
            'delivery_channel': self.delivery_channel,
            'attempts': self.attempts
        }
    
    def __str__(self) -> str:
        return f"Notification(id={self.id}, user={self.user_name}, priority={self.priority})"
    
    def __repr__(self) -> str:
        return self.__str__()
