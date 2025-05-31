from chanels.base import NotificationHandler

class SMSHandler(NotificationHandler):
    def handle(self, user, message):
        if "sms" in user["available"]:
            if self.attempt("SMS", user["name"], message):
                return True
        if self.next_handler:
            return self.next_handler.handle(user, message)
        return False
