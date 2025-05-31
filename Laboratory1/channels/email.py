import random
from .base import ChannelHandler
from logger import Logger

class EmailChannel:
    """
    Canal de notificación por correo electrónico.

    Intenta enviar una notificación al usuario a través de email. Si falla, pasa la solicitud al siguiente canal en la cadena (si existe).

    Args:
        next_handler (ChannelHandler, opcional): El siguiente canal en la cadena de responsabilidad.

    Métodos:
        handle(user, message): Intenta enviar el mensaje por email. Si falla, delega al siguiente canal.
    """
    def __init__(self, next_handler=None):
        """
        Inicializa el canal de email.

        Args:
            next_handler (ChannelHandler, opcional): Siguiente canal a ejecutar si este falla.
        """
        self.next_handler = next_handler

    def handle(self, user, message):
        """
        Maneja el envío de una notificación por email.

        Args:
            user (User): Usuario destinatario.
            message (str): Mensaje a enviar.

        Returns:
            bool: True si el envío fue exitoso, False si fallaron todos los canales.
        """
        logger = Logger()
        # Simula éxito o fallo
        success = random.choice([True, False])
        logger.log(f"Intento de envío por email a {user.name}: {'éxito' if success else 'fallo'} - Mensaje: {message}")
        if success:
            return True
        elif self.next_handler:
            return self.next_handler.handle(user, message)
        return False
