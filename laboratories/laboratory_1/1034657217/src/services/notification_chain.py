from services.channel_handler import EmailHandler, SMSHandler, ConsoleHandler
from model.user import User
from model.usersModel import UsersModel

class NotificationChain:
    def __init__(self):
        user_model = UsersModel()
        self.users_list:list[User] =user_model.giveList()
        self.handlers={
            'email': EmailHandler(),
            'sms': SMSHandler(),
            'console':ConsoleHandler()
        }
        self.chain_start = None
    
    def buildChain(self,user_name:str):
        user:User = next((u for u in self.users_list if u.name == user_name),None)
        if not user:
            return False, "User not found"
        
        last_handler = None

        #Poner el canal preferido primero, si esta
        if user.preferred_channel in user.available_channels and user.preferred_channel in self.handlers:
            preferred_channel = self.handlers[user.preferred_channel]
            self.chain_start = preferred_channel
            last_handler = preferred_channel
        
        # Añadir los otros canales
        for channel in user.available_channels:
            if channel != user.preferred_channel and channel in self.handlers:
                current_handler = self.handlers[channel]
                if self.chain_start is None:
                    self.chain_start = current_handler
                    last_handler = current_handler
                else:
                    last_handler.set_next(current_handler)
                    last_handler = current_handler
        
        if not self.chain_start:
            return False, "No available channels"
    
    def sendNotification(self,notification):
        delivery_success = False
        if self.chain_start:
            delivery_success = self.chain_start.handle(notification)

        if delivery_success:
            return True, "Notification sent"
        else:
            return False, "Failed to send notification"



