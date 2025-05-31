from flask import Blueprint, request, jsonify
from app.patterns.factory import create_channel_chain

api_bp = Blueprint('api', __name__)

# Almacén temporal de usuarios en memoria
users = []

@api_bp.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()

    required_fields = ["name", "preferred_channel", "available_channels"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    user = {
        "name": data["name"],
        "preferred_channel": data["preferred_channel"],
        "available_channels": data["available_channels"]
    }

    users.append(user)
    return jsonify({"message": "User registered successfully", "user": user}), 201

@api_bp.route('/users', methods=['GET'])
def list_users():
    return jsonify(users), 200




@api_bp.route('/notifications/send', methods=['POST'])
def send_notification():
    data = request.get_json()
    user_name = data.get("user_name")
    message = data.get("message")

    # Buscar el usuario por nombre
    user = next((u for u in users if u["name"] == user_name), None)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Construir la lista de canales, primero el preferido, luego los otros
    channels = [user["preferred_channel"]] + [
        ch for ch in user["available_channels"] if ch != user["preferred_channel"]
    ]

    # Crear la cadena de handlers
    handler_chain = create_channel_chain(channels)

    # Intentar enviar el mensaje
    success = handler_chain.handle(message)

    if success:
        return jsonify({"message": "Notification delivered"}), 200
    else:
        return jsonify({"error": "All channels failed"}), 500
