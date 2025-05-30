"""
Strategy Pattern Implementation
Handles different notification priority strategies
"""

from abc import ABC, abstractmethod
from models.notification import Notification

class NotificationStrategy(ABC):
    """
    Abstract strategy for notification processing
    """
    
    @abstractmethod
    def process(self, notification: Notification) -> Notification:
        """
        Process notification based on strategy
        
        Args:
            notification: The notification to process
            
        Returns:
            Processed notification
        """
        pass

class HighPriorityStrategy(NotificationStrategy):
    """
    High priority notification strategy
    Adds urgency indicators and prefixes
    """
    
    def process(self, notification: Notification) -> Notification:
        """
        Process high priority notification
        """
        # Add urgency indicators for high priority
        notification.message = f"🚨 URGENT: {notification.message}"
        return notification

class MediumPriorityStrategy(NotificationStrategy):
    """
    Medium priority notification strategy
    Adds standard indicators
    """
    
    def process(self, notification: Notification) -> Notification:
        """
        Process medium priority notification
        """
        # Add standard indicator for medium priority
        notification.message = f"ℹ️ INFO: {notification.message}"
        return notification

class LowPriorityStrategy(NotificationStrategy):
    """
    Low priority notification strategy
    Adds low priority indicators
    """
    
    def process(self, notification: Notification) -> Notification:
        """
        Process low priority notification
        """
        # Add low priority indicator
        notification.message = f"📝 NOTICE: {notification.message}"
        return notification

class NotificationStrategyContext:
    """
    Context class for notification strategies
    """
    
    def __init__(self):
        self._strategy: NotificationStrategy = None
    
    def set_strategy(self, strategy: NotificationStrategy):
        """
        Set the notification strategy
        
        Args:
            strategy: The strategy to use
        """
        self._strategy = strategy
    
    def process_notification(self, notification: Notification) -> Notification:
        """
        Process notification using the current strategy
        
        Args:
            notification: The notification to process
            
        Returns:
            Processed notification
        """
        if self._strategy:
            return self._strategy.process(notification)
        return notification
