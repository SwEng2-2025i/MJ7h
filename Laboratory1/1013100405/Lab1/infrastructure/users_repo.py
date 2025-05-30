from domain.entities.user import User  

class InMemoryUserRepository():
    def __init__(self):
        self.users = []

    def save(self, user: User) -> None:
        self.users.append(user)

    def list_all(self) -> list[User]:
        return self.users