''' -------------------------------
--------------------------
Esta cosa aun no está bien:
----------------------------
------------------------------
'''


from domain.entities.user import User
from domain.notifications.strategy import NotificationContext, EmailStrategy, SmsStrategy, WhatsappStrategy, InstagramStrategy

CHANNEL_STRATEGIES = {
    "email": EmailStrategy,
    "sms": SmsStrategy,
    "whatsapp": WhatsappStrategy,
    "instagram": InstagramStrategy
}

class NotificationHandler:
    def __init__(self, channel_name:str, strategy_cls, next_handler=None):
        self.channel_name = channel_name
        self.strategy_cls = strategy_cls
        self.next_handler = next_handler

    def handle(self, user, message, priority, logger):
        if self.channel_name in user.available_channels:
            strategy = NotificationContext(self.strategy_cls())
            log = strategy.send(user, message, priority)
            logger.save(entry=log)
        elif self.next_handler:
            self.next_handler.handle(user, message, priority, logger)


def build_handler_chain(user:User):
    channels_order = [user.preferred_channel] + [
        ch for ch in user.available_channels if ch != user.preferred_channel
    ]

    handler = None
    for channel in reversed(channels_order):
        strategy_cls = CHANNEL_STRATEGIES.get(channel)
        if strategy_cls:
            handler = NotificationHandler(channel, strategy_cls, handler)
    return handler

if __name__ == "__chain_responsibility__":
    user = User("jose", "email", ["email", "sms", "whatsapp"])
    handler = build_handler_chain(user)