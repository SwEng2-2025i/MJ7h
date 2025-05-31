from src.utils.logger import logger
from typing import List
from handlers.handler import Handler
from handlers.handler_factory import FactoryHandler

class CreateChain:
    @classmethod
    def create_chain(cls, preferred: str, available: List[str]) -> Handler:
        if preferred not in available:
            raise ValueError("Preferred channel must be in available channels")

        ordered_channels = [preferred] + [ch for ch in available if ch != preferred]

        next_handler = None
        for channel in reversed(ordered_channels):
            handler = FactoryHandler.createHandler(channel)
            handler.set_next(next_handler)
            next_handler = handler

        return next_handler 

