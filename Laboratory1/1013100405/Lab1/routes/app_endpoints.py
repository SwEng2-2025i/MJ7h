from flask import Flask, request, jsonify

from domain.entities.user import User
from infrastructure.users_repo import InMemoryUserRepository

def create_app(user_repo: InMemoryUserRepository):
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

    return app