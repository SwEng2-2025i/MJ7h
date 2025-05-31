import random
from channels.base_channel import BaseChannel
from logger.logger_singleton import Logger

class ConsoleChannel(BaseChannel):
    def send(self, message, user):
        """
        Intenta enviar un mensaje por consola, con 50% de probabilidad de fallo simulado.
        Si falla, pasa al siguiente canal en la cadena.
        """
        Logger().log(f"Intentando mostrar mensaje en consola para {user.name}...")
        if random.choice([True, False]):
            Logger().log(f"✅ Consola: {user.name} -> {message}")
            return True
        else:
            Logger().log(f"❌ Fallo al mostrar en consola a {user.name}")
            if self.next_channel:
                return self.next_channel.send(message, user)
            return False
