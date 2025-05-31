from channels.base_channel import BaseChannel
from logger.logger_singleton import Logger
import random
class EmailChannel(BaseChannel):
    def send(self, message, user):
        """
        Intenta enviar un email, con 50% de probabilidad de fallo simulado.
        Si falla, pasa al siguiente canal en la cadena.
        """
        Logger().log(f"Intentando enviar email a {user.name}...")
        if random.choice([True, False]):
            Logger().log(f"✅ Email enviado a {user.name}: {message}")
            return True
        else:
            Logger().log(f"❌ Fallo al enviar email a {user.name}")
            if self.next_channel:
                return self.next_channel.send(message, user)
            return False
