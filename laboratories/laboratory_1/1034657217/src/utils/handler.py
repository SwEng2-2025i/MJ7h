from abc import ABC, abstractmethod

class Handler(ABC):
    """
    Handler interface
    Abstract class that defines the methods
    to be implemented by each concrete handler
    in the chain of responsability
    """

    def __init__(self):
        self._next_handler = None

    def set_next(self,handler):
        """
        Sets a next handler to form the chain
        """
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self,user,notification:dict):
        """
        If there is a handler in the chain,
        it will proceed to use it
        """
        if self._next_handler:
            return self._next_handler.handle(user,notification)
        return False # no hay más handlers