from typing import Dict, List
from models.user import UserManager
from handlers.concrete_handler import ConcreteNotificationHandler
from factories.strategy_factory import NotificationStrategyFactory
from logger.notification_logger import NotificationLogger
from datetime import datetime

# Servicio principal que gestiona el envío de notificaciones a través de múltiples canales
class NotificationService:
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager  # Instancia para consultar usuarios
        self.logger = NotificationLogger()  # Singleton logger para trazabilidad

    def send_notification(self, user_name: str, message: str, priority: str = "normal") -> Dict:
        """
        Envía una notificación al usuario especificado utilizando una cadena de responsabilidad.
        Se intenta primero el canal preferido, luego los canales restantes si falla.

        :param user_name: Nombre del usuario destinatario
        :param message: Mensaje a enviar
        :param priority: Prioridad de la notificación
        :return: Diccionario con resultado del intento de envío
        """
        # Obtener usuario
        user = self.user_manager.get_user(user_name)
        if not user:
            raise ValueError(f"User {user_name} not found")

        # Construye lista ordenada de canales (preferido primero, luego los otros sin duplicar)
        channels = [user.preferred_channel]
        for channel in user.available_channels:
            if channel not in channels:
                channels.append(channel)

        # Crear manejadores para cada canal y asignar estrategia correspondiente
        handlers: List[ConcreteNotificationHandler] = []
        for channel in channels:
            handler = ConcreteNotificationHandler()
            strategy = NotificationStrategyFactory.create_strategy(channel)
            handler.set_strategy(strategy)
            handlers.append(handler)

        # Encadenar los manejadores (patrón Chain of Responsibility)
        for i in range(len(handlers) - 1):
            handlers[i].set_next(handlers[i + 1])

        # Ejecutar la cadena de manejo: intenta con el primer handler y continúa hasta éxito
        success = False
        if handlers:
            success = handlers[0].handle(user_name, message, priority)

        # Retornar resultado del envío con trazabilidad
        return {
            'user_name': user_name,
            'message': message,
            'priority': priority,
            'success': success,
            'attempted_channels': channels,
            'timestamp': datetime.now().isoformat()
        }
