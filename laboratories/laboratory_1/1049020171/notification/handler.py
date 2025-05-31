from notification.channels import EmailChannel, SMSChannel, ConsoleChannel

class NotificationHandler:
    def __init__(self, user):
        self.user = user
        self.channels = {
            'email': EmailChannel(),
            'sms': SMSChannel(),
            'console': ConsoleChannel()
        }
    
    def handle(self, message, priority):
        # Orden de intentos: canal preferido + alternativos
        for channel_name in [self.user.preferred_channel] + [
            ch for ch in self.user.available_channels 
            if ch != self.user.preferred_channel
        ]:
            channel = self.channels.get(channel_name)
            if channel and channel.send(message):
                return True
        return False