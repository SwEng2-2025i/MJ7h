import random
from domain.entities.user import User
from datetime import datetime
from domain.entities.log_entry import LogEntry


class EmailStrategy:
    def send(self, user: User, message: str, priority: str):
        successful = random.choice([True, False])
        status = "Successful" if successful else "Failed"
        print(f"Notification status: {status}. Via Email to {user.username}. Message: \"{message}\". Priority: {priority}")
        return status

class SmsStrategy:
    def send(self, user: User, message: str, priority: str):
        successful = random.choice([True, False])
        status = "Successful" if successful else "Failed"
        # print(f"Notification status: {status}. Via SMS to {user.phone_number}. Message: \"{message}\". Priority: {priority}")
        log = LogEntry(
            timestamp=str(datetime.now()),
            username=user.username,
            channel="sms",
            message=message,
            priority=priority,
            status=status
        )
        return log


class WhatsappStrategy:
    def send(self, user: User, message: str, priority: str):
        successful = random.choice([True, False])
        status = "Successful" if successful else "Failed"
        # print(f"Notification status: {status}. Via WhatsApp to {user.whatsapp_id}. Message: \"{message}\". Priority: {priority}")
        log = LogEntry(
            timestamp=str(datetime.now()),
            username=user.username,
            channel="whatsapp",
            message=message,
            priority=priority,
            status=status
        )
        return log

class InstagramStrategy:
    def send(self, user: User, message: str, priority: str):
        successful = random.choice([True, False])
        status = "Successful" if successful else "Failed"
        # print(f"Notification status: {status}. Via Instagram to {user.instagram_handle}. Message: \"{message}\". Priority: {priority}")
        log = LogEntry(
            timestamp=str(datetime.now()),
            username=user.username,
            channel="instagram",
            message=message,
            priority=priority,
            status=status
        )
        return log 

class NotificationContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def send(self, user, message, priority):
        return self.strategy.send(user, message, priority)