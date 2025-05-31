import random
from .base_strategy import NotificationStrategy

# Estrategia concreta que implementa el canal de notificación por consola
# Forma parte del patrón Strategy

class ConsoleNotificationStrategy(NotificationStrategy):
    
    def send(self, user_name: str, message: str, priority: str = "normal") -> bool:
        """
        Simula el envío de una notificación al usuario a través del canal 'console'.
        Este canal tiene una tasa de éxito del 75%.

        :param user_name: Nombre del destinatario
        :param message: Mensaje a enviar
        :param priority: Prioridad del mensaje
        :return: True si el mensaje fue enviado exitosamente, False si falló
        """
        # Simula éxito con una probabilidad del 75%
        success = random.choices([True, False], weights=[75, 25])[0]
        
        if success:
            print(f"🖥️  Console notification for {user_name}: {message} (Priority: {priority})")
        else:
            print(f"🖥️  Console notification failed for {user_name}: System busy")
        
        return success

    def get_channel_name(self) -> str:
        """
        Retorna el nombre del canal que esta estrategia representa.

        :return: "console"
        """
        return "console"
