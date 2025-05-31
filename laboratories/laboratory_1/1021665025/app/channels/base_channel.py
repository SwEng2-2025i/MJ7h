from abc import ABC, abstractmethod
import random
from app.utils.logger import logger # Importación directa de la instancia del logger

class BaseChannel(ABC):
    #Clase base abstracta para los canales de notificación.
    def __init__(self):
        self._next_channel: BaseChannel = None # Type hint para claridad

    def set_next(self, channel: 'BaseChannel') -> 'BaseChannel':
        #Establece el siguiente canal en la cadena de responsabilidad.
        self._next_channel = channel
        return channel # Permite encadenamiento: handler1.set_next(handler2).set_next(handler3)

    def send(self, user_name: str, message: str) -> bool:
        #Intenta enviar una notificación a través de este canal.
        #Si el envío simulado a través de `_process_send` es exitoso, retorna True.
        #Si falla y hay un siguiente canal (`_next_channel`), pasa la solicitud a ese canal.
        #Si falla y no hay siguiente canal, retorna False.
        if self._process_send(user_name, message):
            return True
        elif self._next_channel:
            logger.info(f"Canal {self.channel_name()} fallo para '{user_name}'. Intentando con el siguiente canal: {self._next_channel.channel_name() if self._next_channel else 'Ninguno'}.")
            return self._next_channel.send(user_name, message)
        else:
            logger.warning(f"Canal {self.channel_name()} fallo para '{user_name}' y no hay mas canales en la cadena.")
            return False

    @abstractmethod
    def _process_send(self, user_name: str, message: str) -> bool:
        #Método abstracto que debe ser implementado por las subclases.
        #Define la lógica específica de cómo un canal intenta enviar una notificación.
        #Debe simular el éxito o fracaso del envío.
        pass

    @abstractmethod
    def channel_name(self) -> str:
        #Método abstracto que debe retornar el nombre del canal (e.g., 'email', 'sms').
        pass

    def _simulate_failure(self) -> bool:
        #Simula aleatoriamente un fallo en el envío de la notificación.
        #Utiliza `random.choice([True, False])` para determinar el éxito (True) o fallo (False).
        return random.choice([True, False]) 