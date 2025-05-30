class UsersModel:
    def __init__(self):
        self.users_list = []
    
    def addUser(self,newUser):
        self.users_list.append(newUser)
    
    def showAllUsers(self):
        return self.users_list

    def lastUser(self):
        return self.users_list[-1]