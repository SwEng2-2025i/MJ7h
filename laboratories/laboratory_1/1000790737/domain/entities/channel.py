from enum import Enum


class NotificationChannel(Enum):
    EMAIL = "email"
    SMS = "sms"
    APP_NOTIFICATION = "app_notification"
    SMOKE_SIGNAL = "smoke_signal"
    IP_O_AC = "ipoac"  # IP Over Avian Carriers (RFC 1149)
    UNKNOWN = "unknown"
