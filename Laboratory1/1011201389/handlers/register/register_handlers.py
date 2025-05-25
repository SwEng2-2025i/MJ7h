from ..base_handler import BaseHandler

class NameHandler(BaseHandler):
    def handle(self, data):
        if not data.get("name"):
            raise ValueError("'name' parameter is missing")
        return super().handle(data)
    
class PreferredChannelHandler(BaseHandler):
    def handle(self, data):
        if not data.get("preferred_channel"):
            raise ValueError("'preferred_channel' parameter is missing")
        return super().handle(data)
    
class AvailableChannelsHandler(BaseHandler):
    def handle(self, data):
        if not data.get("available_channels"):
            raise ValueError("'available_channels' parameter is missing")
        return super().handle(data)