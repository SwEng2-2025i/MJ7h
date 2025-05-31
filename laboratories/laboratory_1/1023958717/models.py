class User:
    """
    Represents a user in the notification system.
    """
    def __init__(self, name: str, preferred_channel: str, available_channels: list[str]):
        """
        Initializes a new User object.

        Args:
            name (str): The unique name of the user.
            preferred_channel (str): The user's preferred notification channel (e.g., "email", "sms").
            available_channels (list[str]): A list of channels available for the user.
        """
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels

    def to_dict(self):
        """
        Converts the User object to a dictionary.
        """
        return {
            "name": self.name,
            "preferred_channel": self.preferred_channel,
            "available_channels": self.available_channels
        }

class Notification:
    """
    Represents a notification to be sent.
    """
    def __init__(self, user_name: str, message: str, priority: str):
        """
        Initializes a new Notification object.

        Args:
            user_name (str): The name of the user to whom the notification is addressed.
            message (str): The content of the notification message.
            priority (str): The priority of the notification (e.g., "high", "medium", "low").
        """
        self.user_name = user_name
        self.message = message
        self.priority = priority

    def to_dict(self):
        """
        Converts the Notification object to a dictionary.
        """
        return {
            "user_name": self.user_name,
            "message": self.message,
            "priority": self.priority
        }
