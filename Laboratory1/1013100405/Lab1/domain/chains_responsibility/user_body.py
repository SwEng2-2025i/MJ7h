from flask import current_app

# Clase base: Handler
class Handler:
    def __init__(self, next_handler=None):
        self.next = next_handler

    def handle(self, data):
        if self.next:
            return self.next.handle(data)
        
class NewUsernameGivenHandler(Handler):
    def handle(self, data):
        if not data.get("username"):
            return {"message":"Error: username is required", "response":400}
        else:
            return super().handle(data)
class ValidateAvailableChannelsHandler(Handler):
    def handle(self, data):
        # Revisar que no esté vacío
        if not data.get("available_channels"):
            return {"message":"Error: available channels is required", "response":400}
        
        # Revisar que todos los available channels sean validos
        for channel in data["available_channels"]:
            if channel not in current_app.config["STRATEGY_MAP"]:
                return {"message":f"Error: '{channel}' in available channels is not a valid channel", "response":400}        
        # Continuar siguiente handler
        return super().handle(data)

class ValidatePreferredChannelHandler(Handler):
    def handle(self, data):
        # Revisar que no esté vacío
        if not data.get("preferred_channel"):
            return {"message":"Error: preferred channel is required", "response":400}
            
        # Revisar que el preferred channel esté dentro de available channels
        preferredChannel = data["preferred_channel"]
        if preferredChannel not in data["available_channels"]:
            return {"message":f"Error: '{preferredChannel}' in preferred channel is invalid", "response":400}

        # Continuar siguiente handler
        return super().handle(data)

class SuccessHandler(Handler):
    def handle(self, data):
        return {"message":"User request is valid", "response":200}