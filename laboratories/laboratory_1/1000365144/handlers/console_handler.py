from handlers.base_handler import NotificationHandler

class ConsoleHandler(NotificationHandler):
    def can_handle(self, user):
        return "console" in user.get("available_channels", [])

    def send_notification(self, user, message, priority):
        # Actual console output logic would go here
        print(f"Displaying on console for {user['name']}: {message} [Priority: {priority}]")
        return super().send_notification(user, message, priority) 