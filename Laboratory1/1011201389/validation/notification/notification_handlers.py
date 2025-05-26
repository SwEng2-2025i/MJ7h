from ..base_handler import BaseHandler

class UserNameHandler(BaseHandler):
    def handle(self, data):
        user_name = data.get("user_name")

        # Test if it's a non-empty string
        if not isinstance(user_name, str) or not user_name.strip():
            raise ValueError("'user_name' must be a non-empty string")
        return super().handle(data)
    
class MessageHandler(BaseHandler):
    def handle(self, data):
        message = data.get("message")

        # Test if it's a non-empty string
        if not isinstance(message, str) or not message.strip():
            raise ValueError("'message' must be a non-empty string")
        return super().handle(data)
    
class PriorityHandler(BaseHandler):
    def handle(self, data):
        priority = data.get("priority")

        # Test if it's a non-empty string
        if not isinstance(priority, str) or not priority.strip():
            raise ValueError("'priority' must be a non-empty string")
        
        # Test if it's one of the allowed values
        allowed_priorities = ["low", "medium", "high"]
        if priority not in allowed_priorities:
            raise ValueError(f"'priority' must be one of {allowed_priorities}")
        return super().handle(data)