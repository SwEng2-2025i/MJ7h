from channels.email_channel import EmailChannel
from channels.sms_channel import SmsChannel
from models.user import users

def build_channel_chain(available_channels):
    """Construir una cadena de canales de notificación según los canales disponibles del usuario."""
    chain = None

    for channel in reversed(available_channels):
        if channel in available_channels:
            if channel == "email":
                chain = EmailChannel(successor=chain)
            elif channel == "sms":
                chain = SmsChannel(successor=chain)
    return chain
