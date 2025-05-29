from ..notification_handler import NotificationHandler

class SMSHandler(NotificationHandler):
    def handle(self, user, notification):
        # Try to send the SMS notification
        if self.will_be_successful():
            self.log_success(user, notification)
            return "SMS", notification
        self.log_failure(user, notification)
        return super().handle(user, notification)
