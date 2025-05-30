# Módulo que implementa el patrón Factory los canales

from src.channels.email import EmailChannel
from src.channels.sms import SMSChannel
from src.channels.console import ConsoleChannel
from src.channels.channel import Channel

class ChannelFactory:
    @staticmethod
    def create_channel(channel_type: str) -> 'Channel':
        """
        Crea una instancia de un canal según el tipo especificado.
        Implementa el patrón Factory.
        Args:
            channel_type: Tipo de canal ("email", "sms", "console").
        Returns:
            Instancia de un canal (EmailChannel, SMSChannel, ConsoleChannel).
        Raises:
            ValueError: Si el tipo de canal es desconocido.
        """
        channels = {
            "email": EmailChannel,
            "sms": SMSChannel,
            "console": ConsoleChannel
        }
        channel_class = channels.get(channel_type.lower())
        if not channel_class:
            raise ValueError(f"Este canal es desconocido para el sistema: {channel_type}")
        return channel_class()