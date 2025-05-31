from model.usersModel import UsersModel
from model.user import User
from patterns.channel_handlers import EmailHandler,SMSHandler,ConsoleHandler

class NotificationService():
    def __init__(self):
        self.userModel = UsersModel()
        self.handlers = {
            'email':EmailHandler(),
            'sms': SMSHandler(),
            'console':ConsoleHandler()
        }
    
    def userExists(self,name:str):
        user = self.userModel.find_user_by_name(name)
        if user:
            return user
        else:
            raise Exception("User does not exist")
    
    def _checkUserPreferredChannel(self,user:User):
        return user.preferred_channel in user.available_channels and user.preferred_channel in self.handlers
        
    
    def _buildNotificationChain(self,user:User):
        chain_start = None
        last_handler = None
        chain_list = []

        # iniciar cadena con canal preferido, si hay
        if self._checkUserPreferredChannel(user):
           preferred_channel_handler = self.handlers[user.preferred_channel]
           chain_start = preferred_channel_handler
           last_handler = preferred_channel_handler
           chain_list.append(preferred_channel_handler)

        #Añadir los demás canales
        for channel in user.available_channels:
            if channel != user.preferred_channel and channel in self.handlers:
                currentHandler = self.handlers[channel]
                if chain_start == None:
                    chain_start = currentHandler
                    last_handler = currentHandler
                    chain_list.append(currentHandler)
                else:
                    last_handler.set_next(currentHandler)
                    last_handler = currentHandler
                    chain_list.append(currentHandler)
        
        print('*'*50)
        print(f"chain start",chain_start)

        if not chain_start:
            return False, "No available channels"
        
        return chain_start, chain_list


    def sendNotification(self,notification:dict):
        name = notification["user_name"]
        user:User =self.userExists(name)

        notification_chain, chain_list = self._buildNotificationChain(user)
        print(chain_list)

        chain_process_success = notification_chain.handle(user,notification)
        print("process result",chain_process_success)

        if chain_process_success:
            return True, "Notification sent successfully"
        else:
            raise Exception("Failure to send notification")

        