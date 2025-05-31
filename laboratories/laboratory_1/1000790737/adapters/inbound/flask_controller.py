import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from  # type: ignore

from application.services.user_service import UserService
from application.services.notification_service import NotificationService


swagger_config = {  # type: ignore
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,  # type: ignore
            "model_filter": lambda tag: True,  # type: ignore
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

swagger_template = {  # type: ignore
    "swagger": "2.0",
    "info": {
        "title": "Multichannel Notification System API",
        "description": "REST API for managing users and sending notifications through multiple channels with Chain of Responsibility pattern",
        "contact": {
            "name": "Carlos Santiago Sandoval Casallas",
            "email": "csandovalc@unal.edu.co",
        },
        "version": "1.0.0",
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
}


def register_routes(
    app: Flask, user_service: UserService, notification_service: NotificationService
):
    swagger = Swagger(app, config=swagger_config, template=swagger_template)  # type: ignore

    @app.route("/users", methods=["POST"])
    @swag_from("docs/post_users.yml")
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
    @swag_from("docs/get_users.yml")
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
    @swag_from("docs/post_notification_send.yml")
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
