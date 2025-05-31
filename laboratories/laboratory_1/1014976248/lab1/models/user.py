from datetime import datetime
from typing import List, Dict, Optional

# Modelo que representa un usuario del sistema.
class User:
    def __init__(self, name: str, preferred_channel: str, available_channels: List[str]):
        self.name = name  # Nombre del usuario
        self.preferred_channel = preferred_channel  # Canal de notificación preferido
        self.available_channels = available_channels  # Canales disponibles para el usuario
        self.created_at = datetime.now().isoformat()  # Fecha y hora de creación del usuario

    def to_dict(self) -> Dict:
        """
        Convierte el usuario a un diccionario, útil para respuestas API.

        :return: Diccionario con los atributos del usuario
        """
        return {
            'name': self.name,
            'preferred_channel': self.preferred_channel,
            'available_channels': self.available_channels,
            'created_at': self.created_at
        }

# Clase encargada de la gestión de usuarios: registro, consulta y listado.
class UserManager:
    def __init__(self):
        self.users: Dict[str, User] = {}  # Diccionario de usuarios indexado por nombre

    def register_user(self, name: str, preferred_channel: str, available_channels: List[str]) -> User:
        """
        Registra un nuevo usuario con validaciones de canales.

        :raises ValueError: Si ya existe un usuario o hay errores en los canales
        :return: Instancia del nuevo usuario creado
        """
        if name in self.users:
            raise ValueError(f"User {name} already exists")

        # Importa local para evitar dependencias circulares
        from factories.strategy_factory import NotificationStrategyFactory
        valid_channels = NotificationStrategyFactory.get_available_channels()

        if preferred_channel not in valid_channels:
            raise ValueError(f"Invalid preferred channel: {preferred_channel}")

        for channel in available_channels:
            if channel not in valid_channels:
                raise ValueError(f"Invalid channel: {channel}")

        if preferred_channel not in available_channels:
            raise ValueError("Preferred channel must be in available channels")

        user = User(name, preferred_channel, available_channels)
        self.users[name] = user
        return user

    def get_user(self, name: str) -> Optional[User]:
        """
        Obtiene un usuario por nombre.

        :param name: Nombre del usuario
        :return: Objeto User o None si no existe
        """
        return self.users.get(name)

    def get_all_users(self) -> List[User]:
        """
        Devuelve todos los usuarios registrados.

        :return: Lista de objetos User
        """
        return list(self.users.values())

# Instancia única (similar a Singleton manual)
user_manager = UserManager()
