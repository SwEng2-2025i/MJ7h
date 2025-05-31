from typing import List
from strategies.email_strategy import EmailNotificationStrategy
from strategies.sms_strategy import SMSNotificationStrategy
from strategies.console_strategy import ConsoleNotificationStrategy
from strategies.push_strategy import PushNotificationStrategy
from strategies.base_strategy import NotificationStrategy

# Fábrica de estrategias de notificación.
# Implementa el patrón de diseño Factory para instanciar dinámicamente estrategias según el canal.

class NotificationStrategyFactory:
    # Diccionario que asocia nombres de canales con sus clases de estrategia correspondientes
    _strategies = {
        'email': EmailNotificationStrategy,
        'sms': SMSNotificationStrategy,
        'console': ConsoleNotificationStrategy,
        'push': PushNotificationStrategy
    }

    @classmethod
    def create_strategy(cls, channel_type: str) -> NotificationStrategy:
        """
        Crea una instancia de estrategia de notificación según el tipo de canal especificado.

        :param channel_type: Nombre del canal (ej. 'email', 'sms', 'push', etc.)
        :return: Instancia de la clase correspondiente que implementa NotificationStrategy
        :raises ValueError: Si el canal solicitado no está soportado
        """
        if channel_type not in cls._strategies:
            raise ValueError(f"Unknown channel type: {channel_type}")
        return cls._strategies[channel_type]()

    @classmethod
    def get_available_channels(cls) -> List[str]:
        """
        Retorna una lista con los nombres de todos los canales disponibles (claves del diccionario).

        :return: Lista de strings representando los canales disponibles
        """
        return list(cls._strategies.keys())
