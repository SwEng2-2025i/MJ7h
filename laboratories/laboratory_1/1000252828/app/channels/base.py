# Este archivo define la clase base para los canales de comunicación.
class ChannelHandler:
    def __init__(self, name):
        self.name = name
        self.next_channel = None
    # Método para establecer el siguiente canal en la cadena de responsabilidad
    def set_next(self, next_handler):
        self.next_channel = next_handler
        return next_handler
    #  Método para enviar un mensaje, debe ser implementado por las subclases
    def send(self, user_name, message):
        pass