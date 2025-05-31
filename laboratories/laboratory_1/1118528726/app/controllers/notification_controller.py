# app.py
from flask import Flask, jsonify, request
from flask import Blueprint
from functools import wraps
from services.notification_service import build_channel_chain  # Importar el servicio de notificaciones

from models.user import users, user  # Importar el modelo User

notification_bp = Blueprint('notification_bp', __name__)

# Decorador para requerir autorización en las rutas
def require_authorization(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "The Authorization header is missing"}), 401
        return f(*args, **kwargs)   
    return decorated

@notification_bp.route('/send', methods=['POST'])
@require_authorization
def send_notification():
    """
    Send a notification to a user
    ---
    tags:
      - Notifications
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: NotificationSend
          required:
            - user_name
            - message
            - priority
          properties:
            user_name:
              type: string
              description: Name of the user to notify
              example: Juan
            message:
              type: string
              description: Notification message
              example: Your appointment is tomorrow.
            priority:
              type: string
              description: Notification priority (e.g., high, medium, low)
              example: high
      - name: Authorization
        in: header
        type: string
        required: true
        description: Authorization token
    responses:
      200:
        description: Notification sent successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Notification sent successfully
      400:
        description: Missing user_name, message or priority
        schema:
          type: object
          properties:
            error:
              type: string
              example: Missing user_name, message or priority
      401:
        description: Missing Authorization header
        schema:
          type: object
          properties:
            error:
              type: string
              example: The Authorization header is missing
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: User not found
      500:
        description: Failed to send notification
        schema:
          type: object
          properties:
            error:
              type: string
              example: Failed to send notification
    """
    data = request.get_json()

    if not data or 'user_name' not in data or 'message' not in data or 'priority' not in data:
        return jsonify({"error": "Missing user_name, message or priority"}), 400
    
    # Mirar si el usuario existe
    user_found = None 
    for i in users:
        if i.name == data['user_name']:
            user_found = i
            break

    # Mensaje de error si el usuario no existe 
    if not user_found:
        return jsonify({"error": "User not found"}), 404
    
    # extraer el canal preferido y los canales disponibles del usuario
    availeble_chanels = user_found.available_channels
    # Procesar la notificación como una cadena de canales
    chain = build_channel_chain(availeble_chanels)
    sucess = chain.send(user_found, data['message'])
    if sucess:
        return jsonify({"message": "Notification sent successfully"}), 200
    else:
        return jsonify({"error": "Failed to send notification"}), 500
    


