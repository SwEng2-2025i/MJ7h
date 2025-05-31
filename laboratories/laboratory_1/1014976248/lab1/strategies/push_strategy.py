import random
from .base_strategy import NotificationStrategy

# Estrategia concreta para enviar notificaciones vía push (notificaciones emergentes en dispositivos).
# Implementa el patrón Strategy.

class PushNotificationStrategy(NotificationStrategy):

    def send(self, user_name: str, message: str, priority: str = "normal") -> bool:
        """
        Simula el envío de una notificación push al usuario.
        Tiene una probabilidad del 50% de fallar, representando dispositivos sin conexión.

        :param user_name: Nombre del destinatario
        :param message: Contenido del mensaje
        :param priority: Prioridad del mensaje (por defecto: "normal")
        :return: True si la notificación se envía exitosamente, False si falla
        """
        success = random.choice([True, False])  # Simula estado aleatorio del dispositivo

        if success:
            print(f"🔔 Push notification sent to {user_name}: {message} (Priority: {priority})")
        else:
            print(f"🔔 Push notification failed for {user_name}: Device offline")
        
        return success

    def get_channel_name(self) -> str:
        """
        Devuelve el identificador del canal correspondiente a esta estrategia.

        :return: "push"
        """
        return "push"
