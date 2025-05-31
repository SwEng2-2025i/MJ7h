class NotificationPayload:
    #Representa el payload (cuerpo de la solicitud) para enviar una notificación.

    def __init__(self, user_name: str, message: str, priority: str):
        #Inicializa una nueva instancia de NotificationPayload.
        if not user_name:
            raise ValueError("El nombre de usuario no puede estar vacío para la notificacion.")
        if not message:
            raise ValueError("El mensaje de la notificacion no puede estar vacío.")
        # La prioridad podría tener validaciones más específicas si fuera necesario.
        if not priority:
            raise ValueError("La prioridad de la notificacion no puede estar vacía.")

        self.user_name = user_name
        self.message = message
        self.priority = priority

    def __repr__(self) -> str:
        return f"NotificationPayload(user_name='{self.user_name}', message='{self.message}', priority='{self.priority}')"

    def to_dict(self) -> dict:
        return {
            "user_name": self.user_name,
            "message": self.message,
            "priority": self.priority
        } 