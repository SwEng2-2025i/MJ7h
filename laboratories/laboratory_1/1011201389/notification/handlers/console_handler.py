from ..notification_handler import NotificationHandler

class ConsoleHandler(NotificationHandler):
    def handle(self, user, notification):
        # Try to send the console notification
        if self.will_be_successful():
            self.log_success(user, notification)
            return "Console", notification
        self.log_failure(user, notification)
        return super().handle(user, notification)
