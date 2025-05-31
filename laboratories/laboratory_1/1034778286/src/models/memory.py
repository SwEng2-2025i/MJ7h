from models.user import User
from models.notification import Notification

class Memory:

    def __init__(self):
        self.users = []
        self.notifications = []

    def addUser(self, user: User):
        if user not in self.users:
            self.users.append(user)
        else:
            raise ValueError("User already created")

    def getUser(self, name: str):
        for user in self.users:
            if user.name == name:
                return user
        else:
            raise ValueError("User not found")
        
    def addNotification(self, notification: Notification):
        if notification not in self.notifications:
            self.notifications.append(notification)
        else:
            raise ValueError("Notification already created")

        


