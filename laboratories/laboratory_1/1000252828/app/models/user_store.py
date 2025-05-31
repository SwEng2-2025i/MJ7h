# clase que maneja el almacenamiento de usuarios
class UserStore:
    def __init__(self):
        self.users = {}
    # Método para agregar un usuario al almacenamiento
    def add_user(self, name, preferred, available_channels):
        # Verifica si el usuario ya existe
        if name in self.users:
            return False
        self.users[name] = {
            'name': name,
            'preferred_channel': preferred,
            'available_channels': available_channels
        }
        return True
    # 
    def get_user(self, name):
        return self.users.get(name)

    def list_users(self):
        return list(self.users.values())