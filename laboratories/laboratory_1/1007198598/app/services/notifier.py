import random

class NotificationManager:
    def __init__(self, user, message, logger):
        self.user = user
        self.message = message
        self.logger = logger

    def send_notification(self):
        for channel in [self.user.preferred_channel] + self.user.available_channels:
            success = random.choice([True, False])
            self.logger.log(f"Attempted {channel}: {'Success' if success else 'Failure'}")
            if success:
                return True
        return False