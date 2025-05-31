import random
from .base_strategy import NotificationStrategy

# Estrategia concreta que representa el envío de notificaciones por SMS.
# Implementa el patrón Strategy.

class SMSNotificationStrategy(NotificationStrategy):

    def send(self, user_name: str, message: str, priority: str = "normal") -> bool:
        """
        Simula el envío de una notificación por SMS.
        Tiene una probabilidad del 50% de fallo, representando problemas con el proveedor del servicio.

        :param user_name: Nombre del destinatario
        :param message: Texto de la notificación
        :param priority: Prioridad del mensaje (opcional, por defecto "normal")
        :return: True si el SMS fue enviado exitosamente, False si falló
        """
        success = random.choice([True, False])  # Simula disponibilidad del servicio

        if success:
            print(f"📱 SMS sent to {user_name}: {message} (Priority: {priority})")
        else:
            print(f"📱 SMS failed for {user_name}: Service unavailable")

        return success

    def get_channel_name(self) -> str:
        """
        Retorna el nombre del canal asociado a esta estrategia.

        :return: "sms"
        """
        return "sms"
