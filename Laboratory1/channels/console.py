from .base import ChannelHandler

class ConsoleChannel(ChannelHandler):
    def handle(self, user, message):
        if 'console' in user.available_channels:
            print(f"[CONSOLE] Notificación mostrada para {user.name}: {message}")
            return True
        if self.next_handler:
            return self.next_handler.handle(user, message)
        return False