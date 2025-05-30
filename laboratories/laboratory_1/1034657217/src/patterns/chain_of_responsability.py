from abc import ABC, abstractmethod

class ChannelHandler(ABC):
    _next_handler = None

    def set_next(self,handler):
        self._next_handler = handler
        return 
    
    @abstractmethod
    def handle(self,notification):
        if self._next_handler:
            return self._next_handler.handle(notification)
        return False