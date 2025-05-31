from abc import ABC, abstractmethod

class ChannelHandler(ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abstractmethod
    def send(self, user, message):
        pass

    def handle(self, user, message):
        success = self.send(user, message)
        if not success and self.next_handler:
            return self.next_handler.handle(user, message)
        return success