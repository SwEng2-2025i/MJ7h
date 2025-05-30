import random
from patterns.chain_of_responsability import ChannelHandler
from utils.logger import Logger
from model.user import User

class EmailHandler(ChannelHandler):
    def handle(self,notification):
        user:User = notification['user']
        message = notification['message']
        if 'email' in user.available_channels:
            success = random.choice([True,False])
            Logger.log(f"Attempted email notification to {user.name}: '{message}' - {'success' if success else 'failure'}")
            
            if success:
                return True
            else:
                Logger.log(f"Email failed for {user.name}")
                return super().handle(notification)
        return super().handle(notification)

class SMSHandler(ChannelHandler):
    def handle(self,notification):
        user:User = notification['user']
        message = notification['message']
        if 'sms' in user.available_channels:
            success = random.choice([True,False])
            Logger.log(f"Attempted sms notification to {user.name}: '{message}' - {'success' if success else 'failure'}")
            
            if success:
                return True
            else:
                Logger.log(f"sms failed for {user.name}")
                return super().handle(notification)
        return super().handle(notification)

class ConsoleHandler(ChannelHandler):
    def handle(self,notification):
        user:User = notification['user']
        message = notification['message']
        if 'console' in user.available_channels:
            success = random.choice([True,False])
            Logger.log(f"Attempted console notification to {user.name}: '{message}' - {'success' if success else 'failure'}")
            
            if success:
                return True
            else:
                Logger.log(f"console failed for {user.name}")
                return super().handle(notification)
        return super().handle(notification)