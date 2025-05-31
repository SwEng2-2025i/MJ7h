import random
class BaseChannel:
    def __init__(self):
        self.next = None

    def set_next(self, next_handler):
        self.next = next_handler

    def handle(self, preferred, message):
        raise NotImplementedError("Must be implemented by subclass")

    def try_next(self, preferred, message):
        if self.next:
            return self.next.handle(preferred, message)
        return {"status": "failed", "message": "All channels failed."}
