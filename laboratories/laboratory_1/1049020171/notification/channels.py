import random

class NotificationChannel:
    def send(self, message):
        raise NotImplementedError("Método send debe ser implementado")

class EmailChannel(NotificationChannel):
    def send(self, message):
        success = random.choice([True, False])  # Simula fallo aleatorio
        print(f"📧 Email enviado: {message}. Éxito: {success}")
        return success

class SMSChannel(NotificationChannel):
    def send(self, message):
        success = random.choice([True, False])
        print(f"📱 SMS enviado: {message}. Éxito: {success}")
        return success

class ConsoleChannel(NotificationChannel):
    def send(self, message):
        print(f"🖥️ Consola: {message}")
        return True  # Siempre funciona