from flask import Blueprint, request, jsonify, render_template_string
from app.models.user import User
from app.models.notification import Notification
from app.services.channel_handler import get_channel_chain
from app.services.logger import Logger

api_blueprint = Blueprint("api", __name__)
users = {}

@api_blueprint.route('/')
def home():
    html = """
    <h1>Multichannel Notification API</h1>
    <p>API REST corriendo.</p>
    <ul>
      <li><a href="/apidocs/">Documentación Swagger</a></li>
      <li><a href="/users">Ver usuarios (GET /users)</a></li>
    </ul>
    """
    return render_template_string(html)

@api_blueprint.route("/users", methods=["POST"])
def register_user():
    """
    Register a new user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - preferred_channel
            - available_channels
          properties:
            name:
              type: string
            preferred_channel:
              type: string
              enum: ["email", "sms", "console"]
            available_channels:
              type: array
              items:
                type: string
    responses:
      200:
        description: User registered successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: User Juan registered successfully.
      400:
        description: Bad request (missing or invalid fields)
        schema:
          type: object
          properties:
            error:
              type: string
              example: Missing required fields or invalid channel.
      409:
        description: Conflict (user already exists)
        schema:
          type: object
          properties:
            error:
              type: string
              example: User Juan already exists.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    name = data.get("name")
    preferred = data.get("preferred_channel")
    available = data.get("available_channels")

    # Validations
    if not name or not preferred or not available:
        return jsonify({"error": "Missing required fields: name, preferred_channel, or available_channels"}), 400

    if preferred not in ["email", "sms", "console"]:
        return jsonify({"error": "Invalid preferred_channel. Must be one of: email, sms, console"}), 400

    if not isinstance(available, list) or not all(ch in ["email", "sms", "console"] for ch in available):
        return jsonify({"error": "available_channels must be a list containing only: email, sms, console"}), 400

    if name in users:
        return jsonify({"error": f"User {name} already exists."}), 409

    users[name] = User(name, preferred, available)
    return jsonify({"message": f"User {name} registered successfully."})

@api_blueprint.route("/users", methods=["GET"])
def list_users():
    """
    List all users
    ---
    responses:
      200:
        description: A dictionary of all users
        schema:
          type: object
          additionalProperties:
            type: object
            properties:
              preferred_channel:
                type: string
              available_channels:
                type: array
                items:
                  type: string
    """
    return jsonify({name: user.to_dict() for name, user in users.items()})

@api_blueprint.route("/notifications/send", methods=["POST"])
def send_notification():
    """
    Send a notification to a user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - user_name
            - message
            - priority
          properties:
            user_name:
              type: string
            message:
              type: string
            priority:
              type: string
    responses:
      200:
        description: Result of notification attempt
        schema:
          type: object
          properties:
            result:
              type: string
              example: Notification sent via EMAIL
      400:
        description: Bad request (missing fields)
        schema:
          type: object
          properties:
            error:
              type: string
              example: Missing user_name, message or priority
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: User not found
      500:
        description: All notification channels failed
        schema:
          type: object
          properties:
            result:
              type: string
              example: All channels failed for user Juan
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    user_name = data.get('user_name')
    message = data.get('message')
    priority = data.get('priority')

    if not user_name or not message or not priority:
        return jsonify({"error": "Missing user_name, message or priority"}), 400

    user = users.get(user_name)
    if not user:
        return jsonify({"error": "User not found"}), 404

    notification = Notification(user_name, message, priority)
    logger = Logger()
    logger.log(f"Sending notification to {user.name}: {notification.message}")

    success = False
    handler = get_channel_chain(user.available_channels, logger)
    if handler:
        success = handler.handle(user, notification)

    if success:
        return jsonify({"result": f"Notification sent via {notification.channel.upper()}"})
    else:
        return jsonify({"result": f"All channels failed for user {user.name}"}), 500
