from logger import Logger
import random

class SMSChannel:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, user, message):
        logger = Logger()
        success = random.choice([True, False])
        logger.log(f"Intento de envío por SMS a {user.name}: {'éxito' if success else 'fallo'} - Mensaje: {message}")
        if success:
            return True
        elif self.next_handler:
            return self.next_handler.handle(user, message)
        return False