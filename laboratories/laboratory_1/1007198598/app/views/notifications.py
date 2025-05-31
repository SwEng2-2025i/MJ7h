from flask import Blueprint, jsonify, request
from app.services.notifier import NotificationManager
from app.services.logger import Logger
from app.views.users import users

notifications_blueprint = Blueprint('notifications', __name__)

@notifications_blueprint.route('/notifications/send', methods=['POST'])
def send_notification():
    data = request.get_json()
    user_name = data['user_name']
    message = data['message']

    user = next((u for u in users if u.name == user_name), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    logger = Logger.get_instance()
    notifier = NotificationManager(user, message, logger)
    success = notifier.send_notification()

    return jsonify({"success": success})