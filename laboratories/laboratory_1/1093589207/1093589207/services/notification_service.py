from typing import Dict, List, Optional
from channels.notification_channels import create_channel_chain, NotificationChannel
from utils.logger import NotificationLogger

class User:
    def __init__(self, name: str, preferred_channel: str, available_channels: List[str]):
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels

class NotificationService:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.logger = NotificationLogger()
    
    def register_user(self, name: str, preferred_channel: str, available_channels: List[str]) -> bool:
        if not all(channel in ['email', 'sms', 'console'] for channel in available_channels):
            self.logger.error(f"Invalid channels for user {name}")
            return False
            
        if preferred_channel not in available_channels:
            self.logger.error(f"Preferred channel not in available channels for user {name}")
            return False
            
        self.users[name] = User(name, preferred_channel, available_channels)
        self.logger.info(f"User {name} registered successfully")
        return True
    
    def get_users(self) -> List[Dict]:
        return [
            {
                "name": user.name,
                "preferred_channel": user.preferred_channel,
                "available_channels": user.available_channels
            }
            for user in self.users.values()
        ]
    
    def send_notification(self, user_name: str, message: str, priority: str) -> bool:
        if user_name not in self.users:
            self.logger.error(f"User {user_name} not found")
            return False
            
        user = self.users[user_name]
        
        # Create channel chain starting with preferred channel
        channels = [user.preferred_channel] + [
            ch for ch in user.available_channels if ch != user.preferred_channel
        ]
        
        channel_chain = create_channel_chain(channels)
        if not channel_chain:
            self.logger.error(f"No valid channels available for user {user_name}")
            return False
            
        success = channel_chain.notify(user_name, message, priority)
        if success:
            self.logger.info(f"Notification sent successfully to {user_name}")
        else:
            self.logger.error(f"Failed to send notification to {user_name} through any channel")
        
        return success
