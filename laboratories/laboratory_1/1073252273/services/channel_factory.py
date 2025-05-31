
from services.channels import EmailChannel, SMSChannel

def get_channel(channel_name):
    if channel_name == "email":
        return EmailChannel()
    elif channel_name == "sms":
        return SMSChannel()
    else:
        raise ValueError(f"Unsupported channel: {channel_name}")
