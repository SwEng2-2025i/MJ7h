from chanels.base import NotificationHandler

class EmailHandler(NotificationHandler):
    def handle(self, user, message):
        if "email" in user["available"]:
            if self.attempt("Email", user["name"], message):
                return True
        if self.next_handler:
            return self.next_handler.handle(user, message)
        return False
