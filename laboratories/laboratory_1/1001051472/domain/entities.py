from dataclasses import dataclass

# Entidad de dominio que representa a un usuario
@dataclass
class User:
    name: str  # Nombre del usuario
    preferred_channel: str  # Canal preferido para notificaciones
    available_channels: list[str]  # Lista de canales disponibles para el usuario
