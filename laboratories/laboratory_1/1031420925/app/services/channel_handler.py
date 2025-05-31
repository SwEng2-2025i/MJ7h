import random
from app.services.decorators import log_attempts
from app.services.logger import Logger  # Logger singleton para logs

class NotificationHandler:
    """
    Handler que representa un canal específico para enviar notificaciones.
    Implementa el patrón Chain of Responsibility para intentar múltiples canales.
    """
    def __init__(self, channel, logger):
        self.channel = channel  # Canal asociado (email, sms, console, etc.)
        self.logger = logger
        self.next_handler = None  # Siguiente handler en la cadena

    def set_next(self, handler):
        """Establece el siguiente handler en la cadena."""
        self.next_handler = handler

    @log_attempts
    def handle(self, user, notification):
        """
        Intenta enviar la notificación por este canal.
        Simulado con un éxito o fracaso aleatorio.
        Si falla, pasa al siguiente handler.
        """
        success = random.choice([True, False])  # Simulación de envío
        
        if success:
            notification.channel = self.channel  # Registrar canal usado en notificación
            return True
        elif self.next_handler:
            return self.next_handler.handle(user, notification)
        else:
            return False
        
def get_channel_chain(channels, logger=None):
    """
    Construye la cadena de handlers según la lista de canales disponibles.
    Recibe lista de canales y logger (opcional).
    """
    if not channels:
        return None
    logger = logger or Logger()  # Usa logger singleton si no se pasa
    head = NotificationHandler(channels[0], logger)
    current = head
    for ch in channels[1:]:
        handler = NotificationHandler(ch, logger)
        current.set_next(handler)
        current = handler
    return head
