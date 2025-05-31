from chanels.email import EmailHandler
from chanels.sms import SMSHandler
from chanels.console import ConsoleHandler
from models.notification import Notification
from logger.logger import Logger

users = {}

def register_user(data):
    name = data["name"]
    preferred = data["preferred_channel"]
    available = data["available_channels"]
    users[name] = {
        "name": name,
        "preferred": preferred,
        "available": available
    }

def list_users():
    return list(users.values())

def send_notification(data):
    # Validate required fields
    if not data or "user_name" not in data or "message" not in data:
        return {"error": "Invalid notification data"}, 400
    
    # Get notification data
    name = data["user_name"]
    message = data["message"]
    priority = data.get("priority")
    # Log notification
    Logger().log(f"Notification created for {name} with priority {priority}")
    # Validate user exists
    if name not in users:
        return {"error": "User not found"}, 404

    user_info = users[name]


    # Setup Chain of Responsibility
    preferred = user_info["preferred"]
    available = user_info["available"]

    handler_map = {
        "email": EmailHandler(),
        "sms": SMSHandler(),
        "console": ConsoleHandler()
    }

    head = handler_map[preferred]
    current = head
    for channel in available:
        if channel != preferred:
            current = current.set_next(handler_map[channel])

    Logger().log(f"Sending notification to {name}: {message}")
    success = head.handle(user_info, message)
    return {"status": "sent" if success else "failed"}, 200
