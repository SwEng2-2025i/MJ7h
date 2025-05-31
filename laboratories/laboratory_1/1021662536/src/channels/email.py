# Módulo del canal email

from src.channels.channel import Channel
from src.models.notification import Notification
import random

class EmailChannel(Channel):
    def attempt_send(self, notification: 'Notification') -> bool:
        """
        Simula el envío de una notificación por email, éxito o fallo de forma aleatoria.
        """
        success = random.choice([True, False])
        return success