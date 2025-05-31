from flask import Blueprint, request, jsonify
from .models import User
from .services.handlers.email_handler import EmailHandler
from .services.handlers.sms_handler import SMSHandler

bp = Blueprint('routes', __name__)
users = []  # Almacenamos los usuarios en una lista

@bp.route('/users', methods=['POST'])
def register_user():
    data = request.json
    user = User(data['name'], data['preferred_channel'], data['available_channels'])
    users.append(user)
    return jsonify({"message": "User registered successfully"}), 201

@bp.route('/users', methods=['GET'])
def list_users():
    return jsonify([{"name": user.name,
                     "preferred_channel": user.preferred_channel,
                     "available_channels": user.available_channels} for user in users])

@bp.route('/notifications/send', methods=['POST'])
def send_notification():
    data = request.json
    user_name = data['user_name']
    message = data['message']

    user = next((u for u in users if u.name == user_name), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Configuración del Chain of Responsibility
    sms_handler = SMSHandler()
    email_handler = EmailHandler(sms_handler)

    # Enviar notificación
    if email_handler.handle(user, message):
        return jsonify({"message": f"Notification sent to {user_name}"}), 200
    return jsonify({"message": "All channels failed!"}), 500