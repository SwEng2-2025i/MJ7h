from chanels.base import NotificationHandler

class ConsoleHandler(NotificationHandler):
    def handle(self, user, message):
        if "console" in user["available"]:
            if self.attempt("Console", user["name"], message):
                return True
        if self.next_handler:
            return self.next_handler.handle(user, message)
        return False
