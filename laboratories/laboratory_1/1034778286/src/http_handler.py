from flask import Flask, request, jsonify
from src.models.user import User
from src.models.notification import Notification

def create_http_handler(use_case):
    app = Flask(__name__)

    @app.route("/users", methods=["POST"])
    def create_user():
        data = request.json
        try:
            user = User(
                name=data["name"],
                preferred_channel=data["preferred_channel"],
                available_channels=data["available_channels"]
            )
            use_case.create_user(user)
            return jsonify({
                "message": f"User {user.name} created successfully",
                "user_data": {
                    "name": user.name,
                    "preferred_channel": user.preferred_channel,
                    "available_channels": user.available_channels
                }
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/notifications/send", methods=["POST"])
    def send_notification():
        data = request.json
        try:
            user = use_case.get_user_by_name(data["user_name"])
            if not user:
                raise ValueError("User not found")

            notification = Notification(
                user=data["user_name"],
                message=data["message"],
                priority=data["priority"]
            )

            channel_used = use_case.send_notification(notification)

            return jsonify({
                "message": "Notification sent successfully",
                "notification_data": {
                    "user": notification.user,
                    "message": notification.message,
                    "priority": notification.priority
                },
                "channel_used": channel_used
            }), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    return app
