# Módulo del canal SMS

from src.channels.channel import Channel
import random

class SMSChannel(Channel):
    def attempt_send(self, notification: 'Notification') -> bool:
        """
        Simula el envío de una notificación por SMS, éxito o fallo de forma aleatoria.
        """
        success = random.choice([True, False])
        return success