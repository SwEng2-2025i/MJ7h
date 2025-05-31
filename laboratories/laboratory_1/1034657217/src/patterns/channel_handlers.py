from utils.handler import Handler
from utils.logger import Logger
from model.user import User
import random

"""
Concrete implementation of the notification channel's handlers
All share a similar logic
"""
class EmailHandler(Handler):
    def handle(self, user:User,notification:dict):
        logger = Logger()
        message = notification.get("message")
        if 'email' in user.available_channels:
            channel_success = random.choice([True,False])
            logger.log(f"Attempting to notify by email - {user.name}: {message}")

            if channel_success:
                logger.log(f"Success at email - {user.name}") 
                return True
            else:
                logger.log(f"Failure to email {user.name}")
                return super().handle(user,notification)
            
        return super().handle(user,notification) #cuando no esta en los disponibles

class SMSHandler(Handler):
    def handle(self, user:User,notification:dict):
        logger = Logger()
        message = notification.get("message")
        if 'sms' in user.available_channels:
            channel_success = random.choice([True,False])
            logger.log(f"Attempting to notify by sms - {user.name}: {message}")

            if channel_success: # cuando resuelve la notificacion
                logger.log(f"Success at sms - {user.name}") 
                return True
            else:
                logger.log(f"Failure to sms {user.name}") 
                return super().handle(user,notification) # pasa al siguiente
            
        return super().handle(user,notification) #cuando no esta en los disponibles, pasa al siguiente

class ConsoleHandler(Handler):
    def handle(self, user:User,notification:dict):
        logger = Logger()
        message = notification.get("message")
        if 'console' in user.available_channels:
            channel_success = random.choice([True,False])
            logger.log(f"Attempting to notify by console - {user.name}: {message}")

            if channel_success:
                logger.log(f"Success at console - {user.name}") 
                return True
            else:
                logger.log(f"Failure to reach {user.name} by console")
                return super().handle(user,notification)
            
        return super().handle(user,notification) #cuando no esta en los disponibles
            