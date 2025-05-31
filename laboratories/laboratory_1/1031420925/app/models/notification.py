class Notification:
    """
    Representa una notificación a enviar.
    Contiene información del usuario, mensaje y prioridad.
    """
    def __init__(self, user_name: str, message: str, priority: str):
        self.user_name = user_name
        self.message = message
        self.priority = priority
        self.channel = None  # Canal por el cual se envió (rellenado al enviar)

    def to_dict(self):
        return {
            "user_name": self.user_name,
            "message": self.message,
            "priority": self.priority,
            "channel": self.channel
        }
