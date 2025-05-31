class user: 
    def __init__(self, name:str, preferred_channel:str, available_channels:list):
        """Metodo para inicializar un usuario.

        Args:
            name (str): nombre del usuario 
            preferred_channel (_type_): canal Preferido del usuario para recibir notificaciones
            available_channels (_type_): Lista de canales disponibles para el usuario
        """
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels
        
    def to_dict(self):
        return {
            "name": self.name,
            "preferred_channel": self.preferred_channel,
            "available_channels": self.available_channels
        }

users = [
    user("Alice", "email", ["email", "sms"]),
    user("Bob", "sms", ["email", "sms"])
]