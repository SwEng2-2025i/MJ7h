class User:
    """
    Representa un usuario del sistema.
    Tiene nombre, canal preferido y canales disponibles para notificaciones.
    """
    def __init__(self, name, preferred_channel, available_channels):
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels

    def to_dict(self):
        return {
            "name": self.name,
            "preferred_channel": self.preferred_channel,
            "available_channels": self.available_channels,
        }
