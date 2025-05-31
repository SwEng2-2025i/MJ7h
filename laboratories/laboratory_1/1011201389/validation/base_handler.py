class BaseHandler:
    def __init__(self, next_handler=None):
        self.next = next_handler

    def handle(self, data):
        if self.next:
            self.next.handle(data)