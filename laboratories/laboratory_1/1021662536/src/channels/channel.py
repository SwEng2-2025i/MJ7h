# Módulo que define la clase abstracta Channel 
# Presente el patrón Chain of Responsibility

from abc import ABC, abstractmethod
import random
from src.logger.logger import SingletonLogger
from src.models.notification import Notification

class Channel(ABC):
    def __init__(self):
        """
        Inicializa un canal con un logger Singleton y una referencia al siguiente canal.
        """
        self.next_channel = None  # Referencia al siguiente canal en la cadena
        self.logger = SingletonLogger()  # Instancia del logger

    def set_next(self, next_channel: 'Channel') -> 'Channel':
        """
        Establece el siguiente canal en la cadena de responsabilidad --> SECUENCIAL 
        Returns:
            El siguiente canal para permitir encadenamiento.
        """
        self.next_channel = next_channel
        return next_channel

    def send(self, notification: 'Notification') -> bool:
        """
        Patrón Chain of Responsibility.
        Intenta enviar la notificación usando el canal actual. Si falla, pasa al siguiente.
        Args:
            notification: Objeto Notification a enviar.
        Returns:
            True si el envío es exitoso, False si falla.
        """
        success = self.attempt_send(notification)
        self.logger.info(f"Intentando enviar notificación vía {self.__class__.__name__}: {'Éxito' if success else 'Fallo'}")
        if not success and self.next_channel:
            self.logger.info(f"Pasando al siguiente canal: {self.next_channel.__class__.__name__}")
            return self.next_channel.send(notification)
        return success

    @abstractmethod
    def attempt_send(self, notification: 'Notification') -> bool:
        """
        Método abstracto que cada canal concreto debe implementar para simular el envío.
        Args:
            notification: Objeto Notification a enviar.
        Returns:
            True si el envío es exitoso, False si falla.
        """
        pass