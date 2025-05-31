from flask import Blueprint, request, jsonify
from flasgger import swag_from
from services.notification_service import register_user, list_users, send_notification

bp = Blueprint("routes", __name__)

@bp.route("/users", methods=["POST"])
def create_user():
    """
    Register a new user
    ---
    tags:
      - Users
    summary: Register a new user in the notification system
    description: Creates a new user with their preferred notification channel and available channels
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: user
        description: User data to register
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
              description: User's name
              example: "Juan Perez"
            preferred_channel:
              type: string
              description: User's preferred notification channel
              enum: ["email", "sms", "console"]
              example: "email"
            available_channels:
              type: array
              description: List of available notification channels for the user
              items:
                type: string
                enum: ["email", "sms", "console"]
              example: ["email", "sms", "console"]
    responses:
      201:
        description: User registered successfully
        schema:
          type: object
          properties:
            status:
              type: string
              example: "user registered"
      400:
        description: Invalid input data
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid data provided"
    """
    data = request.get_json()
    required_fields = {"name", "preferred_channel", "available_channels"}
    # Validate required fields
    if not data or not required_fields.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400
    # Validate valid channels
    valid_channels = {"email", "sms", "console"}
    if data["preferred_channel"] not in valid_channels or any(ch not in valid_channels for ch in data["available_channels"]):
        return jsonify({"error": "Invalid data provided"}), 400
    # Register user using the service
    register_user(data) 
    return jsonify({"status": "user registered"}), 201

@bp.route("/users", methods=["GET"])
def get_users():
    """
    Get all registered users
    ---
    tags:
      - Users
    summary: Retrieve all registered users
    description: Returns a list of all users registered in the notification system
    produces:
      - application/json
    responses:
      200:
        description: List of users retrieved successfully
        schema:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
                description: User's name
                example: "Juan Perez"
              preferred:
                type: string
                description: User's preferred notification channel
                example: "email"
              available:
                type: array
                description: List of available notification channels
                items:
                  type: string
                example: ["email", "sms", "console"]
        examples:
          application/json:
            - name: "Juan Perez"
              preferred: "email"
              available: ["email", "sms", "console"]
            - name: "Maria Garcia"
              preferred: "sms"
              available: ["sms", "console"]
    """
    return jsonify(list_users())

@bp.route("/notifications/send", methods=["POST"])
def notify():
    """
    Send notification to a user
    ---
    tags:
      - Notifications
    summary: Send a notification to a registered user
    description: Sends a notification message to a user using their preferred channel or fallback channels
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: notification
        description: Notification data
        required: true
        schema:
          type: object
          required:
            - user_name
            - message
          properties:
            user_name:
              type: string
              description: Name of the user to send notification to
              example: "Juan Perez"
            message:
              type: string
              description: Message content to send
              example: "Your order has been shipped!"
            priority:
              type: string
              description: Notification priority level
              example: "high"
    responses:
      200:
        description: Notification sent successfully
        schema:
          type: object
          properties:
            status:
              type: string
              enum: ["sent", "failed"]
              example: "sent"
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User not found"
      400:
        description: Invalid input data
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid notification data"
    """
    data = request.get_json()
    required_fields = {"user_name", "message"}
    # Validate required fields
    if not data or not required_fields.issubset(data):
        return jsonify({"error": "Invalid notification data"}), 400
    
    # Validate optional priority
    valid_priorities = {"low", "medium", "high"}
    priority = data.get("priority")
    if priority and priority not in valid_priorities:
        return jsonify({"error": "Invalid priority value"}), 400
    # Send notification using the service
    response, status_code = send_notification(data)
    return jsonify(response), status_code
