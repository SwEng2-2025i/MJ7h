from .base import ChannelHandler
class SMSChannel(ChannelHandler):
    def __init__(self):
        super().__init__('sms')
    # Método para enviar un mensaje SMS
    def send(self, user_name, message):
        print(f"Enviando SMS a {user_name}: {message}")