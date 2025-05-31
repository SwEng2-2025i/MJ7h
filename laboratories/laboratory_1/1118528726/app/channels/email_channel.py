from .base_channel import BaseChannel
import random
from logger.logger import LoggerSingleton


class EmailChannel(BaseChannel):
    def send(self, user, message):
        """Send an email message to the user."""

        print("Intentando enviar un correo electrónico a", user.name)
        logger = LoggerSingleton()
        logger.log(f"Intentando enviar un correo electrónico a {user.name}")
        # Simulate email sending logic
        choice  = random.choice([True, False])
        if choice:
            print(f"Correo electrónico enviado a {user.name} con el mensaje: {message}")
            logger.log(f"Correo electrónico enviado a {user.name} con el mensaje: {message}")
            return True
        else:
            print(f"Error al enviar el correo electrónico a {user.name}. Intentando con el siguiente canal...")
            logger.log(f"Error al enviar el correo electrónico a {user.name}. Intentando con el siguiente canal...")

            if self.successor:
                return self.successor.send(user, message)
            else:
                print("No hay más canales para intentar.")
                logger.log("No hay más canales para intentar.")
                return False