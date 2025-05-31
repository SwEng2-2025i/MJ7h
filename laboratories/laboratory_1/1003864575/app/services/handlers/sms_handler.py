import random
from .base_handler import ChannelHandler

class SMSHandler(ChannelHandler):
    def send(self, user, message):
        if 'sms' in user.available_channels:
            print(f"Attempting to send SMS to {user.name}...")
            return random.choice([True, False])  # Simula éxito/fallo
        return False