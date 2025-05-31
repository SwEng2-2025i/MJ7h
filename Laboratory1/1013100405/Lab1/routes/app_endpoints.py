from flask import Flask, request, jsonify

from domain.entities.user import User
from infrastructure.users_repo import InMemoryUserRepository
from domain.strategies.notification import NotificationContext, EmailStrategy, SmsStrategy, WhatsappStrategy, InstagramStrategy
from infrastructure.notifications_logger import InMemoryLoggerRepository
from domain.chains_responsibility.notification_body import SuccessHandler, UsernameGivenHandler, MessageGivenHandler, PriorityGivenHandler
from domain.chains_responsibility.notification_channels import TryPreferredChannel, TryOtherChannels
from domain.chains_responsibility.user_body import NewUsernameGivenHandler, ValidateAvailableChannelsHandler, ValidatePreferredChannelHandler, SuccessHandler
STRATEGY_MAP = {
    "email": EmailStrategy,
    "sms": SmsStrategy,
    "whatsapp": WhatsappStrategy,
    "instagram": InstagramStrategy
}

def create_app(user_repo: InMemoryUserRepository, logger:InMemoryLoggerRepository):
    app = Flask(__name__)

    # Volver disponibles estas instancias globalmente (from flask import current_app)
    app.config["USER_REPO"] = user_repo
    app.config["LOGGER"] = logger
    app.config["STRATEGY_MAP"] = STRATEGY_MAP

    @app.route("/users", methods=["POST"])
    def create_user():
        data = request.json

        # Validar que el cuerpo del request sea válido
        user_body_handler = NewUsernameGivenHandler(ValidatePreferredChannelHandler(ValidateAvailableChannelsHandler(SuccessHandler())))
        result = user_body_handler.handle(data)

        # Si la validación falla, devolver el error
        if result["response"] != 200:
            return jsonify(result)
        
        # Crear el user
        user = User(
            username=data["username"],
            preferred_channel=data["preferred_channel"],
            available_channels=data["available_channels"]
        )

        user_repo.save(user)

        # Devolver detalles del user creado
        return jsonify({
            "username": user.username,
            "preferred_channel": user.preferred_channel,
            "available_channels": user.available_channels
        }), 201
    

    @app.route("/users", methods=["GET"])
    def list_users(): # Obtener la lista de users
        users = user_repo.list_all()

        return jsonify(
        [{"username": user.username,
        "preferred_channel": user.preferred_channel,
        "available_channels": user.available_channels
        } for user in users])
    
    @app.route("/notifications/send", methods=["POST"])
    def send_notification():
        data = request.json
        
        # Validad que el cuerpo de la notificacion sea valido
        notification_body_handler = UsernameGivenHandler(MessageGivenHandler(PriorityGivenHandler(SuccessHandler())))
        result = notification_body_handler.handle(data)
        # Si la validación falla, devolver el error
        if result["response"] != 200:
            return jsonify(result)

        # Validar que el user exista
        user = user_repo.get_user(data.get("user_name"))
        if not user:
            return jsonify({"error": "User not found in repository"}), 404
        
        # Lógica para intentar enviar la notificacion por los distintos canales disponibles
        notification_channels_handler = TryPreferredChannel(TryOtherChannels())
        successful = notification_channels_handler.handle(user, data)

        return jsonify({"status": "Notification processed","successfully_sent":successful}), 200

    @app.route("/notifications/logger", methods=["GET"])
    def list_notification_logs(): #Obtener la lista de logs de notificaiones
        logs = logger.list_all()
        return jsonify({"logs": logs}), 200
    
    return app