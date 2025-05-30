"""
Factory Pattern Implementation
Creates notification handlers based on channel type
"""

from typing import Dict, Type
from patterns.chain_of_responsibility import NotificationHandler, EmailHandler, SMSHandler, ConsoleHandler

class NotificationChannelFactory:
    """
    Factory for creating notification channel handlers
    Implements the Factory pattern
    """
    
    def __init__(self):
        """
        Initialize factory with available handlers
        """
        self._handlers: Dict[str, Type[NotificationHandler]] = {
            'email': EmailHandler,
            'sms': SMSHandler,
            'console': ConsoleHandler
        }
    
    def create_handler(self, channel: str) -> NotificationHandler:
        """
        Create a notification handler for the specified channel
        
        Args:
            channel: The notification channel type
            
        Returns:
            NotificationHandler instance for the channel
            
        Raises:
            ValueError: If channel type is not supported
        """
        if channel not in self._handlers:
            raise ValueError(f"Unsupported channel type: {channel}")
        
        handler_class = self._handlers[channel]
        return handler_class()
    
    def get_available_channels(self) -> list:
        """
        Get list of available channel types
        
        Returns:
            List of available channel types
        """
        return list(self._handlers.keys())
    
    def register_handler(self, channel: str, handler_class: Type[NotificationHandler]):
        """
        Register a new handler type
        
        Args:
            channel: The channel name
            handler_class: The handler class to register
        """
        self._handlers[channel] = handler_class
