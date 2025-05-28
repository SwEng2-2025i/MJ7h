from flask import Blueprint, request, jsonify
from app.models.user import User

user_routes = Blueprint('user_routes', __name__)
users = []  # lista en memoria

@user_routes.route('/users', methods=['POST'])
def create_user():
    """
    Register a new user
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: user
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            preferred_channel:
              type: string
            available_channels:
              type: array
              items:
                type: string
    responses:
      201:
        description: User created successfully
      400:
        description: Missing user fields
    """
    data = request.get_json()
    name = data.get('name')
    preferred = data.get('preferred_channel')
    available = data.get('available_channels')

    if not name or not preferred or not available:
        return jsonify({"error": "Missing user fields"}), 400

    new_user = User(name, preferred, available)
    users.append(new_user)
    return jsonify({"message": "User created successfully"}), 201

@user_routes.route('/users', methods=['GET'])
def list_users():
    """
    List all users
    ---
    tags:
      - Users
    responses:
      200:
        description: A list of users
        schema:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
              preferred_channel:
                type: string
              available_channels:
                type: array
                items:
                  type: string
    """
    return jsonify([
        {
            "name": u.name,
            "preferred_channel": u.preferred_channel,
            "available_channels": u.available_channels
        }
        for u in users
    ])
