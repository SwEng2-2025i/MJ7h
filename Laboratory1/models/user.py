class User:
    """
    Representa a un usuario del sistema de notificaciones.

    Atributos:
        name (str): Nombre del usuario.
        preferred_channel (str): Canal preferido para recibir notificaciones (por ejemplo: 'email', 'sms', 'console').
        available_channels (list): Lista de canales disponibles para el usuario.

    Métodos:
        __init__(name, preferred_channel, available_channels): Inicializa una nueva instancia de User.
    """
    def __init__(self, name, preferred_channel, available_channels):
        """
        Inicializa un nuevo usuario.

        Args:
            name (str): Nombre del usuario.
            preferred_channel (str): Canal preferido para notificaciones.
            available_channels (list): Canales disponibles para el usuario.
        """
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels
