import random

class BaseChannel:
    def __init__(self, successor=None):
        """Initialize the base channel with an optional successor."""
        self.successor = successor

    def set_successor(self, successor):
        """Set the successor channel."""
        self.successor = successor
    
    def send(self, user, message ):
                raise NotImplementedError("Implementa este método en las subclases")