import random
from .base_handler import ChannelHandler

class EmailHandler(ChannelHandler):
    def send(self, user, message):
        if 'email' in user.available_channels:
            print(f"Attempting to send email to {user.name}...")
            return random.choice([True, False])  # Simula éxito/fallo
        return False