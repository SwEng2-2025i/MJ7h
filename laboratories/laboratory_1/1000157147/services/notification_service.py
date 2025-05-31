from factories.channel_factory import ChannelFactory
from logger.logger_singleton import Logger

#Servicio principal para manejar notificaciones.
#Implementa el patrón Cadena de Responsabilidad

def build_channel_chain(available_channels, preferred_channel):
    """
    Construye la cadena de responsabilidad para los canales de notificación.
    
    Args:
        available_channels: Lista de canales disponibles del usuario
        preferred_channel: Canal preferido del usuario
    
    Returns:
        Primer eslabón de la cadena o None si no hay canales
    """
    if preferred_channel in available_channels:
        channels = [preferred_channel] + [ch for ch in available_channels if ch != preferred_channel]
    else:
        channels = available_channels

    if not channels:
        return None

    head = ChannelFactory.create_channel(channels[0])
    current = head
    for name in channels[1:]:
        next_channel = ChannelFactory.create_channel(name)
        current.set_next(next_channel)
        current = next_channel
    return head

def send_notification(user, message):
    """
        Intenta enviar una notificación al usuario a través de sus canales disponibles.
    
        Args:
        user: Instancia de User con las preferencias
        message: Contenido de la notificación
    
        Returns:
        bool: True si se envió correctamente, False si falló en todos los canales
    """
    
    Logger().log(f"Iniciando notificación a {user.name}")
    channel_chain = build_channel_chain(user.available_channels, user.preferred_channel)
    return channel_chain.send(message, user)