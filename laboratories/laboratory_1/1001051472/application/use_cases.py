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

        # Construir la cadena de responsabilidad: primero el canal preferido, luego los demás
        channel_map = {
            "email": EmailHandler,
            "sms": SMSHandler,
            "console": ConsoleHandler
        }

        # Ordenar canales: preferido primero, luego los demás sin duplicados
        ordered_channels = [user.preferred_channel] + [ch for ch in user.available_channels if ch != user.preferred_channel]

        chain = None
        # Construir la cadena en el orden correcto
        for channel in reversed(ordered_channels):
            chain = channel_map[channel](chain)

        result = chain.handle(message, self.logger)
        return {"status": "delivered", "via": result} if result != "Failed" else {"status": "failed"}
