class User:
    """Modelo que representa un usuario del sistema de notificaciones"""
    def __init__(self, name, preferred_channel, available_channels):
        """
        Args:
            name: Nombre del usuario
            preferred_channel: Canal de notificación preferido
            available_channels: Lista de canales disponibles para el usuario
        """
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels