import random
from abc import ABC, abstractmethod

class Handler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, request):
        pass

class AbstractHandler(Handler):
    _next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return None

class EmailHandler(AbstractHandler):
    def handle(self, request):
        if "email" in request["user"]["available_channels"]:
            success = random.choice([True, False])
            if success:
                return {
                    "status": "success",
                    "channel": "email",
                    "message": request["message"],
                    "user": request["user"]["name"]
                }
            print(f"Fallo en envío por email. Pasando al siguiente canal...")
            return super().handle(request)  # Pasar al siguiente handler inmediatamente
        return super().handle(request)

class SMSHandler(AbstractHandler):
    def handle(self, request):
        if "sms" in request["user"]["available_channels"]:
            success = random.choice([True, False])
            if success:
                return {
                    "status": "success",
                    "channel": "sms",
                    "message": request["message"],
                    "user": request["user"]["name"]
                }
            print(f"Fallo en envío por SMS. Intentando siguiente canal...")
        return super().handle(request)

class ConsoleHandler(AbstractHandler):
    def handle(self, request):
        if "console" in request["user"]["available_channels"]:
            # El console handler nunca falla (último recurso)
            print(f"NOTIFICACIÓN EN CONSOLA: {request['user']['name']} - {request['message']}")
            return {
                "status": "success",
                "channel": "console",
                "message": request["message"],
                "user": request["user"]["name"]
            }
        return super().handle(request)