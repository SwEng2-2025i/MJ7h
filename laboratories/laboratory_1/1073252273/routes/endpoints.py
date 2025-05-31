
from flask import Blueprint, request, jsonify
from storage.user_store import add_user, get_user, list_users
from services.notifier import notify
from utils.schemas import validate_user_payload, validate_notification_payload

bp = Blueprint("routes", __name__)

@bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    try:
        validate_user_payload(data)
        user = add_user(data["name"], data["preferred_channel"], data["available_channels"])
        return jsonify({"message": f"User {user.name} created"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/users", methods=["GET"])
def list_all_users():
    users = list_users()
    return jsonify([{
        "name": u.name,
        "preferred_channel": u.preferred_channel,
        "available_channels": u.available_channels
    } for u in users])

@bp.route("/notifications/send", methods=["POST"])
def send_notification():
    data = request.get_json()
    try:
        validate_notification_payload(data)
        user = get_user(data["user_name"])
        if not user:
            return jsonify({"error": "User not found"}), 404
        success = notify(user, data["message"], data["priority"])
        if success:
            return jsonify({"message": "Notification sent successfully"}), 200
        else:
            return jsonify({"error": "All channels failed"}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
