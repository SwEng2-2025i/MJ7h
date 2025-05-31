from abc import ABC, abstractmethod

# Interfaz base abstracta que define el contrato para todas las estrategias de notificación
# Forma parte del patrón de diseño Strategy

class NotificationStrategy(ABC):

    @abstractmethod
    def send(self, user_name: str, message: str, priority: str = "normal") -> bool:
        """
        Envía una notificación al usuario especificado.
        Este método debe ser implementado por cada canal concreto (email, sms, etc.).

        :param user_name: Nombre del usuario destinatario
        :param message: Contenido del mensaje a enviar
        :param priority: Prioridad del mensaje (ej. low, normal, high)
        :return: True si el envío fue exitoso, False si falló
        """
        pass

    @abstractmethod
    def get_channel_name(self) -> str:
        """
        Devuelve el nombre del canal que implementa la estrategia.
        Usado para identificar el tipo de estrategia (por ejemplo: "email", "sms", etc.)
        """
        pass
