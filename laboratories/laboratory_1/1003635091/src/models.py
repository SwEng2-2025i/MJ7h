class User:
    """Representa un usuario con sus canales de notificación"""
    
    def __init__(self, name, preferred_channel, available_channels):
        """
        Crea un nuevo usuario
        Args:
            name: Identificador único
            preferred_channel: Canal principal (email/sms/console)
            available_channels: Canales alternativos disponibles
        """
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels
    
    def to_dict(self):
        """Convierte el usuario a diccionario para respuestas API"""
        return {
            'name': self.name,
            'preferred_channel': self.preferred_channel,
            'available_channels': self.available_channels
        }

class Notification:
    """Representa una notificación a enviar"""
    
    def __init__(self, user, message, priority):
        """
        Crea una nueva notificación
        Args:
            user: Usuario destinatario
            message: Contenido del mensaje
            priority: Nivel de prioridad (high/medium/low)
        """
        self.user = user
        self.message = message
        self.priority = priority