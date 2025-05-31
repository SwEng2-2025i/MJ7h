from .base import ChannelHandler
from logger import Logger
import random

class ConsoleChannel:
    """
    Canal de notificación por consola.

    Intenta mostrar una notificación al usuario en consola. Si falla, pasa la solicitud al siguiente canal en la cadena.

    Args:
        next_handler (ChannelHandler, opcional): El siguiente canal en la cadena de responsabilidad.

    Métodos:
        handle(user, message): Intenta mostrar el mensaje por consola. Si falla, delega al siguiente canal.
    """
    def __init__(self, next_handler=None):
        """
        Inicializa el canal de consola.

        Args:
            next_handler (ChannelHandler, opcional): Siguiente canal a ejecutar si este falla.
        """
        self.next_handler = next_handler

    def handle(self, user, message):
        """
        Maneja el envío de una notificación por consola.

        Args:
            user (User): Usuario destinatario.
            message (str): Mensaje a mostrar.

        Returns:
            bool: True si el envío fue exitoso, False si fallaron todos los canales.
        """
        logger = Logger()
        success = random.choice([True, False])
        logger.log(f"Intento de envío por CONSOLE a {user.name}: {'éxito' if success else 'fallo'} - Mensaje: {message}")
        if success:
            return True
        elif self.next_handler:
            return self.next_handler.handle(user, message)
        return False
