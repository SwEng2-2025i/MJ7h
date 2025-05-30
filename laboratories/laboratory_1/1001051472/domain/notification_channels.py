import random

# Manejador base (Chain of Responsibility)
class NotificationHandler:
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, message, logger):
        raise NotImplementedError  # Debe ser implementado por los canales concretos

# Canal específico para Email
class EmailHandler(NotificationHandler):
    def handle(self, message, logger):
        logger.log("Intentando enviar por email...")
        if random.choice([True, False]):
            logger.log("Email enviado exitosamente.")
            return "Email"
        elif self.successor:
            return self.successor.handle(message, logger)
        return "Failed"

# Canal específico para SMS
class SMSHandler(NotificationHandler):
    def handle(self, message, logger):
        logger.log("Intentando enviar por SMS...")
        if random.choice([True, False]):
            logger.log("SMS enviado exitosamente.")
            return "SMS"
        elif self.successor:
            return self.successor.handle(message, logger)
        return "Failed"

# Canal específico para Consola
class ConsoleHandler(NotificationHandler):
    def handle(self, message, logger):
        logger.log("Intentando enviar por console...")
        if random.choice([True, False]):
            logger.log("Console enviado exitosamente.")
            return "Console"
        elif self.successor:
            return self.successor.handle(message, logger)
        return "Failed"
