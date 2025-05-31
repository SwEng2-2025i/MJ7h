from .user import User
from patterns.singleton import Singleton

class UsersModel(Singleton):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.users_list:list[User] = []
            self._initialized = True # Marcar como inicializado
    
    def addUser(self,newUser):
        user = User(newUser["name"],newUser["preferred_channel"], newUser["available_channels"])
        self.users_list.append(user)
    
    def showAllUsers(self):
        all_users = [i.to_dict() for i in self.users_list]
        return all_users

    def lastUser(self):
        return self.users_list[-1].to_dict()
    
    def find_user_by_name(self,name:str)->User:
        print("user list",self.users_list)
        user = next((u for u in self.users_list if u.name == name) ,None)
        return user