import random
from ..utils.logger import LoggerSingleton

logger = LoggerSingleton()

class NotificationHandler:
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    def handle(self, user, message):
        raise NotImplementedError("Subclasses must implement this method")

class EmailHandler(NotificationHandler):
    def handle(self, user, message):
        print(f"Intentando enviar email a {user['name']}...")

        success = random.choice([True, False])
        status = "success" if success else "failed"
        logger.log("email", user, message, status)

        if success:
            return {"channel": "email", "status": "success"}
        else:
            if self.next_handler:
                return self.next_handler.handle(user, message)
            else:
                return {"channel": "email", "status": "failed, no más handlers"}

class SmsHandler(NotificationHandler):
    def handle(self, user, message):
        print(f"Intentando enviar SMS a {user['name']}...")

        success = random.choice([True, False])
        status = "success" if success else "failed"
        logger.log("sms", user, message, status)

        if success:
            return {"channel": "sms", "status": "success"}
        else:
            if self.next_handler:
                return self.next_handler.handle(user, message)
            else:
                return {"channel": "sms", "status": "failed, no más handlers"}
