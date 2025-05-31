import random

class BaseChannel:
    """Clase abstracta que define la interfaz para todos los canales de notificación"""
    def __init__(self):
        self.next_channel = None

    def set_next(self, channel):
        """
        Establece el siguiente canal en la cadena de responsabilidad.
        
        Args:
            channel: Siguiente canal a intentar
        
        Returns:
            El mismo canal para permitir encadenamiento fluido
        """
        self.next_channel = channel
        return channel  # Para encadenar con fluidez

    def send(self, message, user):
        raise NotImplementedError("Debe implementarse en la subclase")
