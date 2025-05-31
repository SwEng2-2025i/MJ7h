from abc import ABC, abstractmethod
from typing import Optional
from strategies.base_strategy import NotificationStrategy

# Clase base abstracta para los manejadores de notificaciones.
# Implementa el patrón de diseño Chain of Responsibility.

class NotificationHandler(ABC):
    def __init__(self):
        # Referencia al siguiente manejador en la cadena
        self._next_handler: Optional['NotificationHandler'] = None
        # Estrategia de envío asociada a este manejador
        self._strategy: Optional[NotificationStrategy] = None

    def set_next(self, handler: 'NotificationHandler') -> 'NotificationHandler':
        """
        Define el siguiente manejador en la cadena.

        :param handler: Siguiente objeto NotificationHandler
        :return: El manejador pasado como parámetro (útil para chaining fluido)
        """
        self._next_handler = handler
        return handler

    def set_strategy(self, strategy: NotificationStrategy):
        """
        Asigna una estrategia de notificación a este manejador.

        :param strategy: Objeto que implementa NotificationStrategy
        """
        self._strategy = strategy

    @abstractmethod
    def handle(self, user_name: str, message: str, priority: str = "normal") -> bool:
        """
        Intenta manejar la notificación con la estrategia actual. 
        Si falla o no hay estrategia, delega en el siguiente manejador.

        :param user_name: Nombre del destinatario
        :param message: Contenido del mensaje
        :param priority: Prioridad del mensaje
        :return: True si se envió exitosamente, False si se agotó la cadena
        """
        pass
