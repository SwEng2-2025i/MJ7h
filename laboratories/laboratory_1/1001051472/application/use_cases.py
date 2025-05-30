from domain.entities import User
from domain.notification_channels import EmailHandler, SMSHandler, ConsoleHandler

# Caso de uso principal para la gestión de notificaciones y usuarios
class NotificationUseCase:
    def __init__(self, user_repo, logger):
        self.user_repo = user_repo  # Repositorio de usuarios (en memoria)
        self.logger = logger        # Logger Singleton

    def register_user(self, name, preferred, available):
        """Registra un nuevo usuario en el sistema."""
        user = User(name=name, preferred_channel=preferred, available_channels=available)
        self.user_repo.add_user(user)

    def list_users(self):
        """Devuelve la lista de usuarios registrados."""
        return self.user_repo.list_users()

    def send_notification(self, user_name, message, priority):
        """Envía una notificación a un usuario usando la cadena de canales."""
        user = self.user_repo.get_user(user_name)
        if not user:
            return {"status": "failed", "reason": "User not found"}

        # Construir la cadena de responsabilidad en orden de los canales disponibles
        channel_map = {
            "email": EmailHandler,
            "sms": SMSHandler,
            "console": ConsoleHandler
        }

        chain = None
        # Se construye la cadena de canales en el orden especificado por el usuario
        for channel in reversed(user.available_channels):
            chain = channel_map[channel](chain)

        result = chain.handle(message, self.logger)
        return {"status": "delivered", "via": result} if result != "Failed" else {"status": "failed"}
