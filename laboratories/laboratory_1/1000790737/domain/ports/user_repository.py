from abc import ABCMeta, abstractmethod
from ..entities.user import User


class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    def user_exists(self, user_name: str) -> bool:
        """Check if a user exists in the repository."""
        pass

    @abstractmethod
    def get_user(self, user_name: str) -> User:
        """Get a user by their user name.
        Returns None if the user does not exist."""
        pass

    @abstractmethod
    def save_user(self, user: User) -> None:
        """Save a user to the repository."""
        pass
