from .handlers.sms_handler import SMSHandler

class NotificationService:
    handlers = {
        'sms': SMSHandler,
    }

    def send_notification(self, user, notification):
        chain = self._build_chain(user)
        try:
            result = chain.handle(user, notification)
            return result
        except ConnectionError as e:
            raise ConnectionError(f"Failed to send notification: {e}")

    def _build_chain(self, user):
        try:
            preferred_handler = self.handlers[user.preferred_channel]
        except KeyError:
            raise ValueError(f"Preferred channel '{user.preferred_channel}' is not available.")
        

        # Obtain the ordered list of handlers, starting with the preferred handler
        ordered_channels = [preferred_handler] + [handler for handler in self.handlers.values() if handler != preferred_handler]


        # Build the chain of handlers
        chain = None
        for handler in reversed(ordered_channels):
            chain = handler(chain)

        return chain