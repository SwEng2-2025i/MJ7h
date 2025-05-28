import random

class NotificationChannel:
    def __init__(self):
        self.next_channel = None

    def set_next(self, next_channel):
        self.next_channel = next_channel

    def send(self, message):
        raise NotImplementedError("Must override send method")
