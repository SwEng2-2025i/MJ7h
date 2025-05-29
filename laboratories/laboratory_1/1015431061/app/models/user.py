class User:
    def __init__(self, id, name, preferred_channel, available_channels):
        self.id = id
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels

    def to_dict(self):
        """Convierte el objeto User a un diccionario"""
        return {
            "id": self.id,
            "name": self.name,
            "preferred_channel": self.preferred_channel,
            "available_channels": self.available_channels
        }