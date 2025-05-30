import random
from app.services.logger import Logger

class NotificationHandler:
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    def handle(self, message):
        raise NotImplementedError("This method must be overridden by subclasses")


class EmailHandler(NotificationHandler):
    def handle(self, message):
        logger = Logger()
        logger.log("Trying to send via Email...")
        if random.choice([True, False]):
            print(f" Email sent: {message}")
            return True
        elif self.next_handler:
            print(" Email failed. Passing to next...")
            return self.next_handler.handle(message)
        else:
            print(" Email failed. No backup available.")
            return False


class SMSHandler(NotificationHandler):
    def handle(self, message):
        logger = Logger()
        logger.log("Trying to send via Email...")
        if random.choice([True, False]):
            print(f" SMS sent: {message}")
            return True
        elif self.next_handler:
            print(" SMS failed. Passing to next...")
            return self.next_handler.handle(message)
        else:
            print(" SMS failed. No backup available.")
            return False


class ConsoleHandler(NotificationHandler):
    def handle(self, message):
        logger = Logger()
        logger.log("Trying to send via Email...")
        if random.choice([True, False]):
            print(f" Console output: {message}")
            return True
        elif self.next_handler:
            print(" Console failed. Passing to next...")
            return self.next_handler.handle(message)
        else:
            print(" Console failed. No backup available.")
            return False
