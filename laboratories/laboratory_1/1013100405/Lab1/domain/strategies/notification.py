import random
from domain.entities.user import User
from datetime import datetime
from domain.entities.log_entry import LogEntry

# To access global instance logger
from flask import current_app

class EmailStrategy:
    def send(self, user, message, priority):
        successful = random.choice([True, False])

        return LogEntry(
            timestamp=str(datetime.now()),
            username=user.username,
            channel="email",
            message=message,
            priority=priority,
            successful=successful
        )
class SmsStrategy:
    def send(self, user: User, message: str, priority: str):
        successful = random.choice([True, False])

        return LogEntry(
            timestamp=str(datetime.now()),
            username=user.username,
            channel="sms",
            message=message,
            priority=priority,
            successful=successful
        )


class WhatsappStrategy:
    def send(self, user: User, message: str, priority: str):
        successful = random.choice([True, False])

        return LogEntry(
            timestamp=str(datetime.now()),
            username=user.username,
            channel="whatsapp",
            message=message,
            priority=priority,
            successful=successful
        )

class InstagramStrategy:
    def send(self, user: User, message: str, priority: str):
        successful = random.choice([True, False])

        return LogEntry(
            timestamp=str(datetime.now()),
            username=user.username,
            channel="instagram",
            message=message,
            priority=priority,
            successful=successful
        )

class NotificationContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def send(self, user, message, priority):
        logger = current_app.config["LOGGER"]
        log = self.strategy.send(user, message, priority)
        logger.save(log)
        return log.successful