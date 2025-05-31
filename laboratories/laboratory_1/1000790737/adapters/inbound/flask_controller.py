import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from application.services.user_service import UserService
from application.services.notification_service import NotificationService

from flask import Flask, request, jsonify


def register_routes(
    app: Flask, user_service: UserService, notification_service: NotificationService
):
    @app.route("/users", methods=["POST"])
    def create_user():  # type: ignore
        data = request.json
        if not data or "user_name" not in data or "preferred_channel" not in data:
            return jsonify({"error": "Invalid input"}), 400
        if "available_channels" not in data:
            return jsonify({"error": "Available channels are required"}), 400
        if not isinstance(data["available_channels"], list):
            return jsonify({"error": "Available channels must be a list"}), 400

        try:
            user = user_service.register_user(
                data["user_name"],
                data["preferred_channel"],
                data["available_channels"],
                phone_number=data.get("phone_number"),
                email=data.get("email"),
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        return (
            jsonify(
                {
                    "message": "User registered",
                    "user": {
                        "user_name": user.user_name,
                        "preferred_channel": user.preferred_channel.value,
                        "available_channels": [
                            channel.value for channel in user.available_channels
                        ],
                        "phone_number": user.phone_number,
                        "email": user.email,
                    },
                }
            ),
            201,
        )

    @app.route("/users", methods=["GET"])
    def list_users():  # type: ignore
        users = user_service.list_users()
        return (
            jsonify(
                {
                    "data": [
                        {
                            "user_name": user.user_name,
                            "preferred_channel": user.preferred_channel.value,
                            "available_channels": [
                                channel.value for channel in user.available_channels
                            ],
                            "phone_number": user.phone_number,
                            "email": user.email,
                        }
                        for user in users
                    ]
                }
            ),
            200,
        )

    @app.route("/notifications/send", methods=["POST"])
    def send_notification():  # type: ignore
        data = request.json
        if not data or "user_name" not in data or "message" not in data:
            return jsonify({"error": "Invalid input"}), 400
        if not isinstance(data["priority"], str):
            return jsonify({"error": "Priority must be a string"}), 400

        try:
            notification = notification_service.send_notification(
                user_name=data["user_name"],
                message=data["message"],
                priority=data.get("priority", "normal"),
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        return jsonify(notification), 201
