
# Módulo que maneja la info de los usuarios como nombre, canal preferido y canales disponibles.

class User:
    def __init__(self, name: str, fav_channel: str, available_channels: list[str]):
        """
        Inicializa un usuario con su nombre, canal preferido y canales disponibles.
        Args:
            name: Nombre del usuario.
            favorite_channel: Canal preferido para notificaciones (ej. "email").
            available_channels: Lista de canales disponibles (ej. ["email", "sms"]).
        """
        self.name = name
        self.fav_channel = fav_channel
        self.available_channels = available_channels

    def to_dict(self) -> dict:
        """
        Convierte el objeto User a un diccionario.
        Returns:
            Diccionario con los datos del usuario.
        """
        return {
            "name": self.name,
            "favorite_channel": self.fav_channel,
            "available_channels": self.available_channels
        }