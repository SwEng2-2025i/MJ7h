from .user import User

class UsersModel:
    def __init__(self):
        self.users_list:list[User] = []
    
    def addUser(self,newUser):
        user = User(newUser["name"],newUser["preferred_channel"], newUser["available_channels"])
        self.users_list.append(user)
    
    def showAllUsers(self):
        all_users = [i.to_dict() for i in self.users_list]
        return all_users

    def lastUser(self):
        return self.users_list[-1].to_dict()
    
    def giveList(self):
        user_list = self.users_list
        return user_list