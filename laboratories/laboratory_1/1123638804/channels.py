import random
from logger import Logger

class NotificationChannel:
    def __init__(self, name):
        self.name = name
        self.next_channel = None

    def set_next(self, channel):
        self.next_channel = channel
        return channel

    def send(self, user, message):
        raise NotImplementedError

class EmailChannel(NotificationChannel):
    def __init__(self):
        super().__init__('email')

    def send(self, user, message):
        logger = Logger()
        success = random.choice([True, False])
        logger.log(f"Attempting EMAIL to {user['name']}: '{message}' - {'Success' if success else 'Failed'}")
        if success:
            return True
        elif self.next_channel:
            return self.next_channel.send(user, message)
        return False

class SMSChannel(NotificationChannel):
    def __init__(self):
        super().__init__('sms')

    def send(self, user, message):
        logger = Logger()
        success = random.choice([True, False])
        logger.log(f"Attempting SMS to {user['name']}: '{message}' - {'Success' if success else 'Failed'}")
        if success:
            return True
        elif self.next_channel:
            return self.next_channel.send(user, message)
        return False

class ConsoleChannel(NotificationChannel):
    def __init__(self):
        super().__init__('console')

    def send(self, user, message):
        logger = Logger()
        success = random.choice([True, False])
        logger.log(f"Attempting CONSOLE to {user['name']}: '{message}' - {'Success' if success else 'Failed'}")
        if success:
            return True
        elif self.next_channel:
            return self.next_channel.send(user, message)
        return False

