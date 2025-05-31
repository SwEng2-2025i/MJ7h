# importamos la clase ChannelHandler desde el módulo base
from .base import ChannelHandler
class EmailChannel(ChannelHandler):
    def __init__(self):
        super().__init__('email')
    #cambia el mensaje y ya
    def send(self, user_name, message):
        print(f"Enviando email a {user_name}: {message}")