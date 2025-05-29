from ..notification_handler import NotificationHandler

class EmailHandler(NotificationHandler):
    def handle(self, user, notification):
        # Try to send the email notification
        if self.will_be_successful():
            self.log_success(user, notification)
            return "Email", notification
        self.log_failure(user, notification)
        super().handle(user, notification)
