from typing import Dict
from core.models import User, Notification

USERS: Dict[str, User] = {}          # key = user.name
NOTIFICATIONS: Dict[str, Notification] = {}   # key = notification.id
