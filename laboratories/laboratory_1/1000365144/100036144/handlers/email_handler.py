from handlers.base_handler import NotificationHandler

class EmailHandler(NotificationHandler):
    def can_handle(self, user):
        return "email" in user.get("available_channels", [])

    def send_notification(self, user, message, priority):
        # Actual email sending logic would go here
        print(f"Sending email to {user['name']}: {message} [Priority: {priority}]")
        return super().send_notification(user, message, priority) 