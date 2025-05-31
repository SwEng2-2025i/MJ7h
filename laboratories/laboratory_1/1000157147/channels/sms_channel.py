import random
from channels.base_channel import BaseChannel
from logger.logger_singleton import Logger

class SMSChannel(BaseChannel):
    def send(self, message, user):
        """
        Intenta enviar un sms, con 50% de probabilidad de fallo simulado.
        Si falla, pasa al siguiente canal en la cadena.
        """
        Logger().log(f"Intentando enviar SMS a {user.name}...")
        if random.choice([True, False]):
            Logger().log(f"✅ SMS enviado a {user.name}: {message}")
            return True
        else:
            Logger().log(f"❌ Fallo al enviar SMS a {user.name}")
            if self.next_channel:
                return self.next_channel.send(message, user)
            return False
