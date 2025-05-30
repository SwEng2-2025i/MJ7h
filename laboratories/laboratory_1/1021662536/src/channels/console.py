# Módulo del canal de consola

from src.channels.channel import Channel
from src.models.notification import Notification
import random

class ConsoleChannel(Channel):
    def attempt_send(self, notification: 'Notification') -> bool:
        """
        Simula el envío de una notificación por consola, éxito o fallo de forma aleatoria . 
        Imprimiendo el mensaje por consola.
        """
        print(f"Notificación por consola: {notification.message}")
        success = random.choice([True, False])
        return success