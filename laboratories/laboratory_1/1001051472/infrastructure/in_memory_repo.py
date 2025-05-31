from domain.entities import User

# Repositorio en memoria para almacenar usuarios
class InMemoryUserRepository:
    def __init__(self):
        self.users = {}  # Diccionario para almacenar usuarios por nombre

    def add_user(self, user: User):
        """Agrega un usuario al repositorio."""
        self.users[user.name] = user

    def get_user(self, name: str) -> User:
        """Obtiene un usuario por su nombre."""
        return self.users.get(name)

    def list_users(self):
        """Devuelve una lista de todos los usuarios registrados."""
        return [vars(u) for u in self.users.values()]
