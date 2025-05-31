from flask import current_app
from domain.entities.log_entry import LogEntry
from domain.entities.user import User
from domain.strategies.notification import NotificationContext, EmailStrategy, SmsStrategy, WhatsappStrategy, InstagramStrategy
from datetime import datetime

# Clase base: Handler
class Handler:
    def __init__(self, next_handler=None):
        self.next = next_handler

    def handle(self, user:User, data):
        if self.next:
            return self.next.handle(user, data)
class TryPreferredChannel(Handler):
    def handle(self, user:User,data):
        # Send notification
        channel = user.preferred_channel
        strategy_cls = current_app.config["STRATEGY_MAP"].get(channel)
        strategy = NotificationContext(strategy_cls())
        successful = strategy.send(user, data.get("message"), data.get("priority")) # Log is saved inside this method

        if successful:
            return successful
        else:
            return super().handle(user, data)

class TryOtherChannels(Handler):
    def handle(self, user:User,data):
        successful = False
        for channel in user.available_channels:
            if channel != user.preferred_channel:
                strategy_cls = current_app.config["STRATEGY_MAP"].get(channel)
                strategy = NotificationContext(strategy_cls())
                successful = strategy.send(user, data.get("message"), data.get("priority")) # Log is saved inside this method
                if successful:
                    break
        
        return successful