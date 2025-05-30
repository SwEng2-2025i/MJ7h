"""
User model for the notification system
"""

from typing import List
from datetime import datetime
import uuid

class User:
    """
    Represents a user in the notification system
    """
    
    def __init__(self, name: str, preferred_channel: str, available_channels: List[str]):
        """
        Initialize a new user
        
        Args:
            name: User's name
            preferred_channel: User's preferred notification channel
            available_channels: List of available notification channels for the user
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels
        self.created_at = datetime.now()
    
    def to_dict(self) -> dict:
        """
        Convert user object to dictionary
        
        Returns:
            Dictionary representation of the user
        """
        return {
            'id': self.id,
            'name': self.name,
            'preferred_channel': self.preferred_channel,
            'available_channels': self.available_channels,
            'created_at': self.created_at.isoformat()
        }
    
    def __str__(self) -> str:
        return f"User(name={self.name}, preferred_channel={self.preferred_channel})"
    
    def __repr__(self) -> str:
        return self.__str__()
