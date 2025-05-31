from model.usersModel import UsersModel
from model.user import User
from patterns.channel_handlers import EmailHandler,SMSHandler,ConsoleHandler

class NotificationService():
    """
    Service that abstract the notification logic
    using the chain of responsability
    """
    def __init__(self):
        """
        Initializes instances 
        """
        self.userModel = UsersModel()
        self.handlers = {
            'email':EmailHandler(),
            'sms': SMSHandler(),
            'console':ConsoleHandler()
        }
    
    def userExists(self,name:str):
        """
        Verifies that the user exists 
        """
        user = self.userModel.find_user_by_name(name)
        if user:
            return user
        else:
            raise Exception("User does not exist")
    
    def _checkUserPreferredChannel(self,user:User):
        return user.preferred_channel in user.available_channels and user.preferred_channel in self.handlers
        
    
    def _buildNotificationChain(self,user:User):
        """
        Builds the chain of responsability
        trying to start by the user's preferred channel, 
        and then adding the rest
        """
        chain_start = None
        last_handler = None

        # iniciar cadena con canal preferido, si hay
        if self._checkUserPreferredChannel(user):
           preferred_channel_handler = self.handlers[user.preferred_channel]
           chain_start = preferred_channel_handler
           last_handler = preferred_channel_handler

        #Añadir los demás canales
        for channel in user.available_channels:
            if channel != user.preferred_channel and channel in self.handlers:
                currentHandler = self.handlers[channel]
                if chain_start == None:
                    chain_start = currentHandler
                    last_handler = currentHandler
                else:
                    last_handler.set_next(currentHandler)
                    last_handler = currentHandler
        

        if not chain_start:
            return False, "No available channels"
        
        return chain_start


    def sendNotification(self,notification:dict):
        """
        Uses the chain of responsability to 
        deliver the notification
        """
        name = notification["user_name"]
        user:User =self.userExists(name)

        #construir cadena de responsabilidad
        notification_chain = self._buildNotificationChain(user)
        #Ejecuta la cadena responsabilidad
        chain_process_success = notification_chain.handle(user,notification)

        if chain_process_success:
            return True, "Notification sent successfully"
        else:
            raise Exception("Failure to send notification")

        