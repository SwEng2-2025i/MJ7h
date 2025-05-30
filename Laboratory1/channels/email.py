import random
from .base import ChannelHandler

class EmailChannel(ChannelHandler):
    def handle(self, user, message):
        if 'email' in user.available_channels:
            success = random.choice([True, False])
            if success:
                print(f"[EMAIL] Notificación enviada a {user.name}: {message}")
                return True
            else:
                print(f"[EMAIL] Falló el envío a {user.name}")
        if self.next_handler:
            return self.next_handler.handle(user, message)
        return False