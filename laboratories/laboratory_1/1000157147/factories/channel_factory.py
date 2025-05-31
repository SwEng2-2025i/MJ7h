from channels.email_channel import EmailChannel
from channels.sms_channel import SMSChannel
from channels.console_channel import ConsoleChannel

class ChannelFactory:
    @staticmethod
    def create_channel(name):
        """
        Crea una instancia del canal solicitado.
        
        Args:
            name: Identificador del canal ('email', 'sms', 'console')
        
        Returns:
            Instancia del canal concreto
        
        Raises:
            ValueError: Si el nombre no corresponde a ningún canal conocido
        """
        if name == "email":
            return EmailChannel()
        elif name == "sms":
            return SMSChannel()
        elif name == "console":
            return ConsoleChannel()
        else:
            raise ValueError(f"Canal desconocido: {name}")