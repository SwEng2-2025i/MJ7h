from flask import current_app

# Clase base: Handler
class Handler:
    def __init__(self, next_handler=None):
        self.next = next_handler

    def handle(self, data):
        if self.next:
            return self.next.handle(data)
class UsernameGivenHandler(Handler):
    def handle(self, data):
        if not data.get("user_name"):
            return {"message":"Error: username is required", "response":400}
        else:
            return super().handle(data)

class MessageGivenHandler(Handler):
    def handle(self, data):
        if not data.get("message"):
            return {"message":"Error: a message is required", "response":400}, {"message":"Error: username is required", "response":400}
        else:
            return super().handle(data)

class PriorityGivenHandler(Handler):
    def handle(self, data):
        if not data.get("priority"):
            return {"message":"Error: priority is required", "response":400}
        else:
            return super().handle(data)
class SuccessHandler(Handler):
    def handle(self, data):
        return {"message":"Notification request is valid", "response":200}       