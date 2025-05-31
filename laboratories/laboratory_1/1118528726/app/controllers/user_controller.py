# app.py
from flask import Flask, jsonify, request
from flask import Blueprint
from functools import wraps

from models.user import users, user  # Importar el modelo User


user_bp = Blueprint('user_bp', __name__)


# Decorador para requerir autorización en las rutas
def require_authorization(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "The Authorization header is missing"}), 401
        return f(*args, **kwargs)   
    return decorated

@user_bp.route('/', methods=['GET'])
@require_authorization
def get_users():
    """
    Get all users
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: True
        description: Authorization token
    responses:
      200:
        description: A list of users
        examples:
          application/json: [{"name":"Alice","preferred_channel":"email","available_channels":["email","sms"]}]
      401:
        description: Missing Authorization header
    """
    return  jsonify([u.to_dict() for u in users]), 200

@user_bp.route('/', methods=['POST'])
@require_authorization
def register_user():
    """
    Create a new user
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: User
          required:
            - name
            - preferred_channel
            - available_channels
          properties:
            name:
              type: string
              description: Name of the user
              example: Charlie
            preferred_channel:
              type: string
              items:
                type: string
              description: Preferred channel for notifications
              example: email
            available_channels:
              type: array
              items:
                type: string
              description: Available channels for the user 
              example: ["email", "sms"]
      - name: Authorization
        in: header
        type: string
        required: True
        description: Authorization token
    responses:
      201:
        description: User created
      400:
        description: Invalid input
      401:
        description: Missing Authorization header
    """
    data = request.get_json()
    if not data or "name" not in data or "preferred_channel" not in data or "available_channels" not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_user = user(data["name"], data["preferred_channel"], data["available_channels"])
    
    # agregar el nuevo usuario a la lista de usuarios
    users.append(new_user)

    return jsonify({
        "name": new_user.name,
        "preferred_channel": new_user.preferred_channel,
        "available_channels": new_user.available_channels
    }), 201
    