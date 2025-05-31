from ..base_handler import BaseHandler

class NameHandler(BaseHandler):
    def handle(self, data):
        name = data.get("name")

        # Test if it's an non-empty string
        if not isinstance(name, str) or not name.strip():
            raise ValueError("'name' must be a non-empty string")
        return super().handle(data)

    
class PreferredChannelHandler(BaseHandler):
    def handle(self, data):
        channel = data.get("preferred_channel")

        # Test if it's a non-empty string
        if not isinstance(channel, str) or not channel.strip():
            raise ValueError("'preferred_channel' must be a non-empty string")
        return super().handle(data)

    
class AvailableChannelsHandler(BaseHandler):
    def handle(self, data):
        channels = data.get("available_channels")

        if not isinstance(channels, list) or not channels:
            raise ValueError("'available_channels' must be a non-empty list")

        if not all(isinstance(ch, str) and ch.strip() for ch in channels):
            raise ValueError("All items in 'available_channels' must be non-empty strings")

        return super().handle(data)

    
class PreferredInAvailableChannelsHandler(BaseHandler):
    def handle(self, data):
        preferred_channel = data.get("preferred_channel")
        available_channels = data.get("available_channels")

        if preferred_channel not in available_channels:
            raise ValueError("The preferred channel must be included in 'available_channels'")

        return super().handle(data)
