"""
Chain of Responsibility Pattern Implementation
Handles notification delivery through different channels with fallback support
"""

from abc import ABC, abstractmethod
from typing import Optional
import random
from models.notification import Notification
from models.user import User
from patterns.singleton import NotificationLogger

class NotificationHandler(ABC):
    """
    Abstract base class for notification handlers
    Implements the Chain of Responsibility pattern
    """
    
    def __init__(self):
        self._next_handler: Optional[NotificationHandler] = None
        self.logger = NotificationLogger()
    
    def set_next(self, handler: 'NotificationHandler') -> 'NotificationHandler':
        """
        Set the next handler in the chain
        
        Args:
            handler: The next handler to set
            
        Returns:
            The handler that was set
        """
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, notification: Notification, user: User) -> bool:
        """
        Handle the notification request
        
        Args:
            notification: The notification to send
            user: The target user
            
        Returns:
            True if notification was successfully delivered, False otherwise
        """
        if self._next_handler:
            return self._next_handler.handle(notification, user)
        return False

class EmailHandler(NotificationHandler):
    """
    Handles email notifications
    """
    
    def handle(self, notification: Notification, user: User) -> bool:
        """
        Attempt to send notification via email
        """
        notification.add_attempt()
        self.logger.log(f"Attempting to send notification {notification.id} via EMAIL to {user.name}")
          # Simulate random failure
        success = random.choice([True, False])
        
        if success:
            notification.mark_delivered('email')
            self.logger.log(f"[SUCCESS] EMAIL delivery successful for notification {notification.id}")
            return True
        else:
            self.logger.log(f"[FAILED] EMAIL delivery failed for notification {notification.id}")
            return super().handle(notification, user)

class SMSHandler(NotificationHandler):
    """
    Handles SMS notifications
    """
    
    def handle(self, notification: Notification, user: User) -> bool:
        """
        Attempt to send notification via SMS
        """
        notification.add_attempt()
        self.logger.log(f"Attempting to send notification {notification.id} via SMS to {user.name}")
        
        # Simulate random failure
        success = random.choice([True, False])
        
        if success:
            notification.mark_delivered('sms')
            self.logger.log(f"✅ SMS delivery successful for notification {notification.id}")
            return True
        else:
            self.logger.log(f"❌ SMS delivery failed for notification {notification.id}")
            return super().handle(notification, user)

class ConsoleHandler(NotificationHandler):
    """
    Handles console notifications (always succeeds as fallback)
    """
    
    def handle(self, notification: Notification, user: User) -> bool:
        """
        Send notification via console (always succeeds)
        """
        notification.add_attempt()
        self.logger.log(f"Attempting to send notification {notification.id} via CONSOLE to {user.name}")
        
        # Console delivery always succeeds (fallback)
        notification.mark_delivered('console')
        self.logger.log(f"✅ CONSOLE delivery successful for notification {notification.id}")
        print(f"📱 CONSOLE NOTIFICATION for {user.name}: {notification.message}")
        return True

class NotificationChain:
    """
    Manages the chain of notification handlers
    """
    
    def __init__(self):
        self.first_handler: Optional[NotificationHandler] = None
        self.last_handler: Optional[NotificationHandler] = None
    
    def add_handler(self, handler: NotificationHandler):
        """
        Add a handler to the chain
        
        Args:
            handler: The handler to add
        """
        if not self.first_handler:
            self.first_handler = handler
            self.last_handler = handler
        else:
            self.last_handler.set_next(handler)
            self.last_handler = handler
    
    def handle(self, notification: Notification, user: User) -> bool:
        """
        Process notification through the chain
        
        Args:
            notification: The notification to send
            user: The target user
            
        Returns:
            True if notification was delivered, False otherwise
        """
        if self.first_handler:
            return self.first_handler.handle(notification, user)
        return False
