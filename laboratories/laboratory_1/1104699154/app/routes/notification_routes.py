from flask import Blueprint, request, jsonify
from app.routes.user_routes import users
from app.channels.email import EmailChannel
from app.channels.sms import SMSChannel
from app.channels.console import ConsoleChannel

notification_routes = Blueprint('notification_routes', __name__)

@notification_routes.route('/notifications/send', methods=['POST'])
def send_notification():
    """
    Send a notification to a user
    ---
    tags:
      - Notifications
    parameters:
      - in: body
        name: notification
        required: true
        schema:
          type: object
          properties:
            user_name:
              type: string
            message:
              type: string
    responses:
      200:
        description: Notification sent
      404:
        description: User not found
      400:
        description: No valid channels found
      500:
        description: All channels failed
    """
    data = request.get_json()
    user_name = data.get("user_name")
    message = data.get("message")

    user = next((u for u in users if u.name == user_name), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Map channel names to objects
    channel_map = {
        "email": EmailChannel(),
        "sms": SMSChannel(),
        "console": ConsoleChannel()
    }

    # Crear la cadena de canales en el orden del usuario
    head = None
    prev = None
    for ch_name in user.available_channels:
        ch = channel_map.get(ch_name)
        if not ch:
            continue
        if not head:
            head = ch
        if prev:
            prev.set_next(ch)
        prev = ch

    if head:
        result = head.send(message)
        if result:
            return jsonify({"message": "Notification sent"}), 200
        else:
            return jsonify({"message": "All channels failed"}), 500
    else:
        return jsonify({"error": "No valid channels found"}), 400
