from src.utils.logger import logger
from src.handlers.handler import Handler
from src.handlers.handler_email import EmailHandler
from src.handlers.handler_sms import SMSHandler
from src.handlers.handler_console import ConsoleHandler

class FactoryHandler:
    @staticmethod

    def createHandler(channel: str):
        channels = {"email": EmailHandler, 
                    "sms": SMSHandler,
                    "console": ConsoleHandler}
        
        handler = channels.get(channel.lower())
        if not handler:
            raise ValueError(f"The channel: {channel} is unkown")
        return handler()