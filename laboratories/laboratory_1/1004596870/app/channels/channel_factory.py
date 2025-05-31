from channels.email_channel import EmailChannel
from channels.sms_channel import SmsChannel
from channels.console_channel import ConsoleChannel

class ChannelFactory:
    def create_channel(self, channel_type):
        if channel_type == "email":
            return EmailChannel()
        elif channel_type == "sms":
            return SmsChannel()
        elif channel_type == "console":
            return ConsoleChannel()
        else:
            raise ValueError("Invalid channel type")