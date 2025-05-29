from app.models.user import User

class UserService:
    def __init__(self):
        self.users = []
        self.next_id = 1  # Contador para IDs

    def register_user(self, name, preferred_channel, available_channels):
        """Registra un nuevo usuario y devuelve el objeto User"""
        user = User(
            id=self.next_id,
            name=name,
            preferred_channel=preferred_channel,
            available_channels=available_channels
        )
        self.users.append(user)
        self.next_id += 1
        return user

    def get_user_by_id(self, user_id):
        """Obtiene un usuario por su ID"""
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def get_user_by_name(self, name):
        """Obtiene un usuario por su nombre (case insensitive)"""
        for user in self.users:
            if user.name.lower() == name.lower():
                return user
        return None

    def get_all_users(self):
        """Devuelve todos los usuarios como diccionarios"""
        return [user.to_dict() for user in self.users]