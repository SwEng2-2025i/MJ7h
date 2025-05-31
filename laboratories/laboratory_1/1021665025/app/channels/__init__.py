# Permite que el directorio 'channels' sea tratado como un paquete.
from .base_channel import BaseChannel
from .email_channel import EmailChannel
from .sms_channel import SmsChannel
from .whatsapp_channel import WhatsappChannel

# Factoría para crear instancias de canales basados en su nombre
CHANNEL_FACTORY = {
    "email": EmailChannel,
    "sms": SmsChannel,
    "whatsapp": WhatsappChannel
} 