import random
from .base_strategy import NotificationStrategy

# Estrategia concreta que implementa el canal de notificación por correo electrónico.
# Aplica el patrón Strategy, permitiendo enviar notificaciones simuladas por email.

class EmailNotificationStrategy(NotificationStrategy):

    def send(self, user_name: str, message: str, priority: str = "normal") -> bool:
        """
        Simula el envío de una notificación por email al usuario especificado.
        El éxito o fallo del envío es aleatorio (50/50), representando posibles fallos de red.

        :param user_name: Nombre del destinatario
        :param message: Contenido del mensaje
        :param priority: Prioridad de la notificación
        :return: True si se envió correctamente, False si falló
        """
        success = random.choice([True, False])  # Simulación: 50% éxito, 50% error

        if success:
            print(f"📧 Email sent to {user_name}: {message} (Priority: {priority})")
        else:
            print(f"📧 Email failed for {user_name}: Network error")
        
        return success

    def get_channel_name(self) -> str:
        """
        Devuelve el identificador del canal de esta estrategia.

        :return: "email"
        """
        return "email"
