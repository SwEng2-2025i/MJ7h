from channels import EmailChannel, SMSChannel, ConsoleChannel, NotificationChannel
from models import User
from logger import Logger

class ChannelChainBuilder:
    """
    Builds the Chain of Responsibility for notification channels based on user preferences.
    """
    def __init__(self):
        self.logger = Logger.get_instance()
        # Map channel names to their respective class constructors
        self.channel_map = {
            "email": EmailChannel,
            "sms": SMSChannel,
            "console": ConsoleChannel
        }

    def build_chain(self, user: User) -> NotificationChannel:
        """
        Constructs a chain of notification handlers for a given user.
        The chain prioritizes the preferred channel, followed by other available channels.

        Args:
            user (User): The user for whom to build the notification channel chain.

        Returns:
            NotificationChannel: The head of the constructed chain of handlers, or None if no valid channels.
        """
        # Determine the order of channels: preferred first, then others from available
        ordered_channels = []

        # Add preferred channel first if it's available
        if user.preferred_channel in user.available_channels and user.preferred_channel in self.channel_map:
            ordered_channels.append(user.preferred_channel)
        
        # Add other available channels that are not the preferred one, maintaining order if possible
        for channel_name in user.available_channels:
            if channel_name != user.preferred_channel and channel_name in self.channel_map:
                ordered_channels.append(channel_name)
        
        # Remove duplicates while preserving order (e.g., if preferred is also in available)
        # Using a set to track seen channels and a list for ordered unique channels
        seen_channels = set()
        unique_ordered_channels = []
        for channel in ordered_channels:
            if channel not in seen_channels:
                unique_ordered_channels.append(channel)
                seen_channels.add(channel)

        if not unique_ordered_channels:
            self.logger.log(f"No valid or available channels found for user {user.name}.")
            return None

        # Build the chain
        head_handler = None
        current_handler = None

        for channel_name in unique_ordered_channels:
            try:
                channel_class = self.channel_map[channel_name]
                new_handler = channel_class()
                if head_handler is None:
                    head_handler = new_handler
                    current_handler = new_handler
                else:
                    current_handler.set_next(new_handler)
                    current_handler = new_handler
                self.logger.log(f"Added {channel_name} to the chain for user {user.name}.")
            except KeyError:
                self.logger.log(f"Warning: Unknown channel '{channel_name}' specified for user {user.name}. Skipping.")
            except Exception as e:
                self.logger.log(f"Error creating channel handler for {channel_name}: {e}")
                
        return head_handler