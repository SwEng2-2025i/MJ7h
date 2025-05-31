from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException
from .schemas.user_schema import UserSchema
from .schemas.notification_schema import NotificationSchema
from .handlers.handler import EmailHandler, SmsHandler
from .utils.logger import LoggerSingleton

main_bp = Blueprint('main', __name__)
users = []
logger = LoggerSingleton()

user_schema = UserSchema()
notification_schema = NotificationSchema()

@main_bp.route('/users', methods=['POST'])
def register_user():
    json_data = request.get_json()
    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    users.append(data)
    return jsonify({"message": "User registered successfully."}), 201

@main_bp.route('/users', methods=['GET'])
def list_users():
    return jsonify(users)

@main_bp.route('/notifications/send', methods=['POST'])
def send_notification():
    json_data = request.get_json()
    try:
        data = notification_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user_name = data["user_name"]
    message = data["message"]
    priority = data["priority"]

    user = next((u for u in users if u["name"] == user_name), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    channels = user.get("available_channels", [])
    handlers = []

    for channel in channels:
        if channel == "email":
            handlers.append(EmailHandler())
        elif channel == "sms":
            handlers.append(SmsHandler())

    for i in range(len(handlers) - 1):
        handlers[i].set_next(handlers[i + 1])

    if not handlers:
        return jsonify({"error": "No available channels"}), 400

    preferred_channel = user.get("preferred_channel")
    start_handler = None

    for handler in handlers:
        if handler.__class__.__name__.lower().startswith(preferred_channel):
            start_handler = handler
            break

    if not start_handler:
        start_handler = handlers[0]

    result = start_handler.handle(user, message)

    return jsonify({
        "message": f"Notification attempt finished via {result['channel']}",
        "status": result["status"]
    })

@main_bp.route('/logs', methods=['GET'])
def get_logs():
    return jsonify(logger.get_logs())

# Manejo global de errores HTTP
@main_bp.app_errorhandler(HTTPException)
def handle_http_exception(e):
    response = {
        "error": e.name,
        "message": e.description
    }
    return jsonify(response), e.code

# Manejo global de errores no esperados
@main_bp.app_errorhandler(Exception)
def handle_exception(e):
    print(f"Error inesperado: {e}")
    response = {
        "error": "Internal Server Error",
        "message": str(e)
    }
    return jsonify(response), 500