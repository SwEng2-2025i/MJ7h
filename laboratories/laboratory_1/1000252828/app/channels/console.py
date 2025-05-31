from .base import ChannelHandler
class ConsoleChannel(ChannelHandler):
    def __init__(self):
        super().__init__('console')
    # Método para enviar un mensaje a la consola
    def send(self, user_name, message):
        print(f"Console: Notification for {user_name}: {message}")