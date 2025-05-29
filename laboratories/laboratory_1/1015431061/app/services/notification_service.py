from app.patterns.chain_of_responsibility import EmailHandler, SMSHandler, ConsoleHandler
from app.patterns.singleton import Logger

class NotificationService:
    def __init__(self, user_service):
        self.user_service = user_service
        self.logger = Logger()
        self.setup_handlers()

    def setup_handlers(self):
        # Configurar la cadena de responsabilidad
        self.handler_chain = EmailHandler()
        self.handler_chain \
            .set_next(SMSHandler()) \
            .set_next(ConsoleHandler())

    def send_notification(self, user_id, message, priority):
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            self.logger.log(f"Usuario no encontrado: ID {user_id}")
            return {"status": "error", "message": "User not found"}

        request = {
            "user": {
                "name": user.name,
                "preferred_channel": user.preferred_channel,
                "available_channels": user.available_channels
            },
            "message": message,
            "priority": priority
        }

        self.logger.log(f"Intentando enviar notificación a {user.name} via {user.preferred_channel}")

        # Intentar primero con el canal preferido
        preferred_channel = user.preferred_channel
        handler_map = {
        "email": EmailHandler(),
        "sms": SMSHandler(),
        "console": ConsoleHandler()
        }

        if preferred_channel in handler_map:
            result = handler_map[preferred_channel].handle(request)
            if result and result["status"] == "success":
                return result

        # Si falla, usar la cadena completa
        return self.handler_chain.handle(request) or {
        "status": "error",
        "message": "All delivery attempts failed"
    }

        return {
            "status": "error",
            "message": "No available channels for delivery",
            "attempted_channels": user.available_channels
        }