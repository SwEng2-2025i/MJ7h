import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from typing import List

from domain.entities.user import User
from domain.entities.channel import NotificationChannel
from domain.ports.user_repository import IUserRepository

from application.exceptions import UserAlreadyExistsException, UserNotFoundException


class UserService:
    """Service for managing users."""

    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

    def register_user(
        self,
        user_name: str,
        prefered_channel: str,
        available_channels: List[str],
        phone_number: str | None = None,
        email: str | None = None,
    ) -> User:
        """Register a new user."""
        if self.user_repository.exists(user_name):
            raise UserAlreadyExistsException(
                f"User with the username: '{user_name}', already exists."
            )

        t_prefered_channel = NotificationChannel(prefered_channel)
        t_available_channels = [
            NotificationChannel(channel) for channel in available_channels
        ]
        user = User(
            user_name, t_prefered_channel, t_available_channels, phone_number, email
        )
        self.user_repository.save(user)
        return user

    def list_users(self) -> List[User]:
        """List all users."""
        return self.user_repository.get_all()

    def is_user_registered(self, user_name: str) -> bool:
        """Check if a user is registered."""
        return self.user_repository.exists(user_name)

    def get_user(self, user_name: str) -> User:
        """Get a user by username."""
        user = self.user_repository.get(user_name)
        if not user:
            raise UserNotFoundException(f"User {user_name} not found.")
        return user

    def get_available_channels(self, user_name: str) -> List[NotificationChannel]:
        """Get available channels for a user."""
        user = self.get_user(user_name)
        return user.available_channels
