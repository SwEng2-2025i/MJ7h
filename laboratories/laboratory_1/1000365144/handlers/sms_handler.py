from handlers.base_handler import NotificationHandler

class SMSHandler(NotificationHandler):
    def can_handle(self, user):
        return "sms" in user.get("available_channels", [])

    def send_notification(self, user, message, priority):
        # Actual SMS sending logic would go here
        print(f"Sending SMS to {user['name']}: {message} [Priority: {priority}]")
        return super().send_notification(user, message, priority) 