from flask import Flask, request, jsonify

from domain.entities.user import User
from infrastructure.users_repo import InMemoryUserRepository
from domain.strategies.notification import NotificationContext, EmailStrategy, SmsStrategy, WhatsappStrategy, InstagramStrategy
from infrastructure.notifications_logger import InMemoryLoggerRepository
from domain.chains_responsibility.notification_body import SuccessHandler, UsernameGivenHandler, MessageGivenHandler, PriorityGivenHandler

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

    @app.route("/users", methods=["POST"])
    def create_user():
        data = request.json
        # Validaciones básicas
        if not data or "username" not in data or "preferred_channel" not in data or "available_channels" not in data:
            return jsonify({"error": "Missing fields"}), 400
        
        user = User(
            username=data["username"],
            preferred_channel=data["preferred_channel"],
            available_channels=data["available_channels"]
        )

        user_repo.save(user)

        return jsonify({
            "username": user.username,
            "preferred_channel": user.preferred_channel,
            "available_channels": user.available_channels
        }), 201
    

    @app.route("/users", methods=["GET"])
    def list_users():
        users = user_repo.list_all()
        return jsonify(
        [{"username": user.username,
        "preferred_channel": user.preferred_channel,
        "available_channels": user.available_channels
        } for user in users])
    
    @app.route("/notifications/send", methods=["POST"])
    def send_notification():
        data = request.json
        
        notification_body_handler = UsernameGivenHandler(MessageGivenHandler(PriorityGivenHandler(SuccessHandler())))
        result = notification_body_handler.handle(data)
        if result["response"] != 200:
            return jsonify(result)

        user = user_repo.get_user(data.get("user_name"))
        if not user:
            return jsonify({"error": "User not found in repository"}), 404
        
        channel = user.preferred_channel.lower()
        strategy_cls = STRATEGY_MAP.get(channel)
        strategy = NotificationContext(strategy_cls())
        successful = strategy.send(user, data.get("message"), data.get("priority")) # strategy.send(user, message, priority)

        if not successful:
            for channel in user.available_channels:
                if channel != user.preferred_channel:
                    strategy_cls = STRATEGY_MAP.get(channel)
                    strategy = NotificationContext(strategy_cls())
                    successful = strategy.send(user, data.get("message"), data.get("priority"))
                    if successful:
                        break

        return jsonify({"status": "Notification processed","successfully_sent":successful}), 200

    @app.route("/notifications/logger", methods=["GET"])
    def list_notification_logs():
        logs = logger.list_all()
        return jsonify({"logs": logs}), 200
    
    return app