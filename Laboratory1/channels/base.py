class ChannelHandler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, user, message):
        raise NotImplementedError("Debes implementar este método en las subclases.")