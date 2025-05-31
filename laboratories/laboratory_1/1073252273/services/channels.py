
import random

class NotificationChannel:
    def send(self, user, message):
        raise NotImplementedError()

class EmailChannel(NotificationChannel):
    def send(self, user, message):
        success = random.choice([True, False])
        print(f"[Email] Sending to {user.name}: {message} -> {'Success' if success else 'Fail'}")
        return success

class SMSChannel(NotificationChannel):
    def send(self, user, message):
        success = random.choice([True, False])
        print(f"[SMS] Sending to {user.name}: {message} -> {'Success' if success else 'Fail'}")
        return success
