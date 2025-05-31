from flask import Blueprint, jsonify, request
from app.models.user import User

users_blueprint = Blueprint('users', __name__)

# Simulación de una base de datos en memoria
users = []

@users_blueprint.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()
    user = User(data['name'], data['preferred_channel'], data['available_channels'])
    users.append(user)
    return jsonify({"message": "User registered successfully!"}), 201

@users_blueprint.route('/users', methods=['GET'])
def list_users():
    return jsonify([{
        "name": user.name,
        "preferred_channel": user.preferred_channel,
        "available_channels": user.available_channels
    } for user in users])