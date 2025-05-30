"""
Unit tests for the notification system
"""

import sys
import os
import unittest
import json

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, users_storage
from models.user import User
from models.notification import Notification
from patterns.singleton import NotificationLogger
from patterns.strategy import HighPriorityStrategy, MediumPriorityStrategy, LowPriorityStrategy, NotificationStrategyContext
from patterns.factory import NotificationChannelFactory

class TestNotificationSystem(unittest.TestCase):
    """
    Test cases for the notification system
    """
    
    def setUp(self):
        """
        Set up test environment
        """
        self.app = app.test_client()
        self.app.testing = True
        users_storage.clear()
    
    def test_user_registration(self):
        """
        Test user registration endpoint
        """
        user_data = {
            "name": "Juan",
            "preferred_channel": "email",
            "available_channels": ["email", "sms"]
        }
        
        response = self.app.post('/users', 
                               data=json.dumps(user_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Juan')
        self.assertEqual(data['preferred_channel'], 'email')
    
    def test_user_list(self):
        """
        Test user listing endpoint
        """
        # Register a user first
        user_data = {
            "name": "Maria",
            "preferred_channel": "sms",
            "available_channels": ["sms", "console"]
        }
        
        self.app.post('/users', 
                     data=json.dumps(user_data),
                     content_type='application/json')
        
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Maria')
    
    def test_notification_send(self):
        """
        Test notification sending endpoint
        """
        # Register a user first
        user_data = {
            "name": "Carlos",
            "preferred_channel": "email",
            "available_channels": ["email", "sms", "console"]
        }
        
        self.app.post('/users', 
                     data=json.dumps(user_data),
                     content_type='application/json')
        
        # Send notification
        notification_data = {
            "user_name": "Carlos",
            "message": "Test message",
            "priority": "high"
        }
        
        response = self.app.post('/notifications/send',
                               data=json.dumps(notification_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertIn('notification_id', data)
    
    def test_singleton_logger(self):
        """
        Test singleton pattern for logger
        """
        logger1 = NotificationLogger()
        logger2 = NotificationLogger()
        
        # Both should be the same instance
        self.assertIs(logger1, logger2)
    
    def test_strategy_pattern(self):
        """
        Test strategy pattern for notification priorities
        """
        notification = Notification("test_user", "Test message", "high")
        
        # Test high priority strategy
        context = NotificationStrategyContext()
        context.set_strategy(HighPriorityStrategy())
        processed = context.process_notification(notification)
        self.assertIn("🚨 URGENT:", processed.message)
        
        # Test medium priority strategy
        notification2 = Notification("test_user", "Test message", "medium")
        context.set_strategy(MediumPriorityStrategy())
        processed2 = context.process_notification(notification2)
        self.assertIn("ℹ️ INFO:", processed2.message)
        
        # Test low priority strategy
        notification3 = Notification("test_user", "Test message", "low")
        context.set_strategy(LowPriorityStrategy())
        processed3 = context.process_notification(notification3)
        self.assertIn("📝 NOTICE:", processed3.message)
    
    def test_factory_pattern(self):
        """
        Test factory pattern for creating handlers
        """
        factory = NotificationChannelFactory()
        
        # Test creating different handlers
        email_handler = factory.create_handler('email')
        sms_handler = factory.create_handler('sms')
        console_handler = factory.create_handler('console')
        
        self.assertIsNotNone(email_handler)
        self.assertIsNotNone(sms_handler)
        self.assertIsNotNone(console_handler)
        
        # Test invalid channel
        with self.assertRaises(ValueError):
            factory.create_handler('invalid_channel')

if __name__ == '__main__':
    unittest.main()
