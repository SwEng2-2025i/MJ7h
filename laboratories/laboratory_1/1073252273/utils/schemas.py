
def validate_user_payload(data):
    if not all(k in data for k in ("name", "preferred_channel", "available_channels")):
        raise ValueError("Invalid user payload")

def validate_notification_payload(data):
    if not all(k in data for k in ("user_name", "message", "priority")):
        raise ValueError("Invalid notification payload")
