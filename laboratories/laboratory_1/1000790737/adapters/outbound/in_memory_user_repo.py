import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from domain.ports.user_repository import IUserRepository
from domain.entities.user import User


class InMemoryUserRepository(IUserRepository):
    """In-memory implementation of the user repository."""

    def __init__(self):
        self.users: dict[str, User] = {}

    def save(self, user: User) -> None:
        """Save a user to the repository."""
        self.users[user.user_name] = user

    def get(self, user_name: str) -> User | None:
        """Get a user by username."""
        return self.users.get(user_name)

    def exists(self, user_name: str) -> bool:
        """Check if a user exists in the repository."""
        return user_name in self.users

    def get_all(self) -> list[User]:
        """Get all users in the repository."""
        return list(self.users.values())
