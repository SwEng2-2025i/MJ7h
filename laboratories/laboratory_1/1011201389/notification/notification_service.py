from .handlers.sms_handler import SMSHandler
from .handlers.email_handler import EmailHandler
from .handlers.console_handler import ConsoleHandler

class NotificationService:

    # Handlers available for sending notifications
    handlers = {
        'sms': SMSHandler,
        'email': EmailHandler,
        'console': ConsoleHandler
    }

    # Send a notification to a user
    def send_notification(self, user, notification):

        chain = self._build_chain(user)
        try:
            result = chain.handle(user, notification)
            return result
        except ConnectionError as e:
            raise ConnectionError(f"Failed to send notification: {e}") 

    # Build the chain of handlers based on the user's preferences
    def _build_chain(self, user):
        try:
            preferred_handler = self.handlers[user.preferred_channel]
            available_handlers = [self.handlers[channel] for channel in user.available_channels]
        except KeyError:
            raise ValueError(f"There are some unavailable channels for user {user.name}. Please check the available channels.")
        

        # Obtain the ordered list of handlers, starting with the preferred handler
        ordered_channels = [preferred_handler] + [handler for handler in available_handlers if handler != preferred_handler]


        # Build the chain of handlers
        chain = None
        for handler in reversed(ordered_channels):
            chain = handler(chain)

        return chain