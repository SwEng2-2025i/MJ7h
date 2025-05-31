from handlers import EmailHandler, SMSHandler, ConsoleHandler

# In-memory storage for users
users_db = {}

class NotificationService:
    def __init__(self):
        # Define the default chain of responsibility
        self.handler_chain = EmailHandler(SMSHandler(ConsoleHandler()))

    def register_user(self, name, preferred_channel, available_channels):
        if name in users_db:
            return None # User already exists
        users_db[name] = {
            "name": name,
            "preferred_channel": preferred_channel,
            "available_channels": available_channels
        }
        return users_db[name]

    def get_all_users(self):
        return list(users_db.values())

    def send_notification(self, user_name, message, priority):
        user = users_db.get(user_name)
        if not user:
            return False, "User not found"

        # Dynamically build the chain based on user preference
        preferred = user.get("preferred_channel")
        chain = None

        # Create a map of channel names to handler classes
        handler_map = {
            "email": EmailHandler,
            "sms": SMSHandler,
            "console": ConsoleHandler
        }

        # Build chain starting with preferred channel, then others
        if preferred in handler_map:
            current_handler = handler_map[preferred]()
            chain = current_handler
            for channel_name in user.get("available_channels", []):
                if channel_name != preferred and channel_name in handler_map:
                    current_handler.set_next(handler_map[channel_name]())
                    current_handler = current_handler._next_handler
        else: # If preferred not valid or not set, use default order from available
            first_handler_added = False
            temp_current_handler = None
            for channel_name in user.get("available_channels", []):
                if channel_name in handler_map:
                    if not first_handler_added:
                        chain = handler_map[channel_name]()
                        temp_current_handler = chain
                        first_handler_added = True
                    else:
                        temp_current_handler.set_next(handler_map[channel_name]())
                        temp_current_handler = temp_current_handler._next_handler
        
        if not chain: # Fallback to default chain if no valid channels found for user
            chain = self.handler_chain

        success = chain.handle(user, message, priority)
        return success, f"Notification processed. Success: {success}" 