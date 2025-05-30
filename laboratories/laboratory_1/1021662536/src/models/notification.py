# Módulo que define la clase Notification para representar notificaciones

class Notification:
    def __init__(self, user_name: str, message: str, priority: str):
        """ Inicializa una notificación con el usuario destino, mensaje y prioridad."""
        
        self.user_name = user_name
        self.message = message
        self.priority = priority