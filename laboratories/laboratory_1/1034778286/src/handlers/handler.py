from __future__ import annotations  

class Handler:
    def __init__(self, next_handler: Handler = None):
        self.next = next_handler

    def handle(self, data):
        if self.next:
            self.next.handle(data)
        else:
            raise ValueError("The notification could not be sent")

    def set_next(self, next_handler: Handler):
        self.next = next_handler