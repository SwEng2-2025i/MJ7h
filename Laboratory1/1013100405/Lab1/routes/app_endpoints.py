from flask import Flask, request, jsonify

from domain.entities.user import User
from infrastructure.users_repo import InMemoryUserRepository
from domain.notifications.strategy import NotificationContext, EmailStrategy, SmsStrategy, WhatsappStrategy, InstagramStrategy
from infrastructure.notifications_logger import InMemoryLoggerRepository

def create_app(user_repo: InMemoryUserRepository, logger:InMemoryLoggerRepository):
    app = Flask(__name__)

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
        username = data.get("user_name")
        message = data.get("message")
        priority = data.get("priority")

        if not data or not username or not message or not priority:
            return jsonify({"error": "Missing required fields"}), 400

        # Algorithm
        user = user_repo.get_user(username)
        if not user:
            return jsonify({"error": "User not found"}), 404

        strategy = None
        for channel in user.available_channels:
            if channel == "email":
                strategy = NotificationContext(EmailStrategy())
            elif channel == "sms":
                strategy = NotificationContext(SmsStrategy())
            elif channel == "whatsapp":
                strategy = NotificationContext(WhatsappStrategy())
            elif channel == "instagram":
                strategy = NotificationContext(InstagramStrategy())
            log = strategy.send(user, message, priority)
            logger.save(entry=log)

        return jsonify({"status": "Notification processed"}), 200
    
    @app.route("/logger", methods=["GET"])
    def get_logger():
        logs = logger.list_all()
        return jsonify(logs), 200

    return app