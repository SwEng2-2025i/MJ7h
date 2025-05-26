class Notification():
    def __init__(self, user_name, message, priority):
        self.user_name = user_name
        self.message = message
        self.priority = priority

    @classmethod
    def from_dict(cls, data):
        user_name = data.get("user_name")
        message = data.get("message")
        priority = data.get("priority")

        return Notification(user_name, message, priority)
    
    def to_dict(self):
        return {
            "user_name": self.user_name,
            "message": self.message,
            "priority": self.priority
        }