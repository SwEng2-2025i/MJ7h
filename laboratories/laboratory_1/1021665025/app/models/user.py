from typing import List

class User:
    #Representa a un usuario del sistema de notificaciones.
    def __init__(self, name: str, preferred_channel: str, available_channels: List[str]):
        #Inicializa una nueva instancia de Usuario.
        if not name:
            raise ValueError("El nombre de usuario no puede estar vacío.")
        if not preferred_channel:
            raise ValueError("El canal preferido no puede estar vacío.")
        if not available_channels:
            raise ValueError("La lista de canales disponibles no puede estar vacía.")
        if preferred_channel not in available_channels:
            raise ValueError(f"El canal preferido '{preferred_channel}' debe estar en la lista de canales disponibles: {available_channels}")

        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels

    def __repr__(self) -> str:
        return f"User(name='{self.name}', preferred_channel='{self.preferred_channel}', available_channels={self.available_channels})"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "preferred_channel": self.preferred_channel,
            "available_channels": self.available_channels
        } 