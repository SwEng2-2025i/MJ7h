from abc import ABCMeta, abstractmethod
from ..entities.user import User


class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    def exists(self, user_name: str) -> bool:
        """Check if a user exists in the repository."""
        pass

    @abstractmethod
    def get(self, user_name: str) -> User:
        """Get a user by their user name.
        Returns None if the user does not exist."""
        pass

    @abstractmethod
    def get_all(self) -> list[User]:
        """Get all users in the repository."""
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        """Save a user to the repository."""
        pass
