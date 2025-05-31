from src.models.user import User
from src.models.notification import Notification
from src.models.memory import Memory
from src.handlers.createChain import CreateChain

class UseCase:

    def __init__(self, memory: Memory):
        self.memory = memory

    def create_user(self, user: User):
        self.memory.addUser(user)

    def get_user_by_name(self, name: str) -> User:
        return self.memory.getUser(name)

    def send_notification(self, notification: Notification):
        self.memory.addNotification(notification)
        user = self.get_user_by_name(notification.user)
        if user:
            handler = CreateChain.create_chain(user.preferred_channel, user.available_channels)
            handler.handle(notification)
        else:
            raise ValueError("User not found for notification")
