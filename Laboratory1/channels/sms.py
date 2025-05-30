import random
from .base import ChannelHandler

class SMSChannel(ChannelHandler):
    def handle(self, user, message):
        if 'sms' in user.available_channels:
            success = random.choice([True, False])
            if success:
                print(f"[SMS] Notificación enviada a {user.name}: {message}")
                return True
            else:
                print(f"[SMS] Falló el envío a {user.name}")
        if self.next_handler:
            return self.next_handler.handle(user, message)
        return False