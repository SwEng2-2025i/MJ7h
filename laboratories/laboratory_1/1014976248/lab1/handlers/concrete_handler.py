from logger.notification_logger import NotificationLogger
from .base_handler import NotificationHandler

# Manejador concreto que intenta enviar una notificación con su estrategia asignada.
# Si falla, pasa el control al siguiente manejador en la cadena.
# Implementa el patrón Chain of Responsibility.

class ConcreteNotificationHandler(NotificationHandler):

    def handle(self, user_name: str, message: str, priority: str = "normal") -> bool:
        """
        Intenta enviar una notificación usando la estrategia configurada.
        Registra el intento mediante el singleton NotificationLogger.
        Si falla y hay otro manejador, delega en él.

        :param user_name: Nombre del destinatario
        :param message: Contenido de la notificación
        :param priority: Nivel de prioridad del mensaje
        :return: True si alguna estrategia logra enviar el mensaje, False si todas fallan
        """
        logger = NotificationLogger()

        if self._strategy:
            channel_name = self._strategy.get_channel_name()
            success = self._strategy.send(user_name, message, priority)
            
            # Se registra el intento, exitoso o no
            logger.log_attempt(user_name, channel_name, message, success, priority)

            if success:
                return True  # Éxito, no se continúa la cadena

        # Si no hay estrategia o falló el envío, se delega en el siguiente handler
        if self._next_handler:
            return self._next_handler.handle(user_name, message, priority)

        return False  # No se pudo enviar por ningún canal
