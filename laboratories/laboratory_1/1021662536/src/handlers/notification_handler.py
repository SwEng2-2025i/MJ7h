# Módulo que maneja las notificaciones usando la cadena de canales (chain of responsibility).

from src.channels.factory import ChannelFactory
from src.logger.logger import SingletonLogger
from src.models.user import User
from src.models.notification import Notification

class NotificationHandler:
    def __init__(self):
        """
        Inicializa el manejador con un logger Singleton.
        """
        self.logger = SingletonLogger()

    def send_notification(self, user: 'User', notification: 'Notification') -> bool:
        """
        Envía una notificación al usuario usando la cadena de canales.
        Args:
            user: Objeto User con los canales disponibles y favorito.
            notification: Objeto Notification a enviar.
        Returns:
            True si la notificación se envía con éxito, False si falla.
        """
        # Creación de la cadena de canales usando el Factory
        channels = [ChannelFactory.create_channel(channel) for channel in user.available_channels]
        
        # Establecer la cadena de responsabilidad
        for i in range(len(channels) - 1):
            channels[i].set_next(channels[i + 1])
        
        # Encontrar el índice del canal favorito del usuario
        preferred_index = next((i for i, channel in enumerate(channels) if channel.__class__.__name__.lower() == user.fav_channel), 0)
        
        # Envío desde el canal favorito 
        self.logger.info(f"Enviando notificación a {user.name} vía canal favorito: {user.fav_channel}")
        success = channels[preferred_index].send(notification)
        
        if success:
            self.logger.info(f"Notificación enviada con éxito a {user.name}")
        else:
            self.logger.error(f"Fallo al enviar notificación a {user.name}")
        return success