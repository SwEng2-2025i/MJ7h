from ..notification_handler import NotificationHandler

class SMSHandler(NotificationHandler):
    def handle(self, user, notification):
        # Try to send the SMS notification
        if self.will_be_successful():
            self.log(f"SMS sent to {user.name}: {notification}")
            return "SMS", notification
        self.log(f"Failed to send SMS to {user.name}")
        super().handle(user, notification)
