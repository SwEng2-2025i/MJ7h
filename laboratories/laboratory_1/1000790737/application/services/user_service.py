import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from typing import List

from domain.entities.user import User
from domain.entities.channel import NotificationChannel
from domain.ports.user_repository import IUserRepository

from application.exceptions import UserAlreadyExistsException


class UserService:
    """Service for managing users."""

    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

    def register_user(
        self,
        user_name: str,
        prefered_channel: NotificationChannel,
        available_channels: List[NotificationChannel],
    ) -> User:
        """Register a new user."""
        if self.user_repository.exists(user_name):
            raise UserAlreadyExistsException(
                f"User with the username: '{user_name}', already exists."
            )

        user = User(user_name, prefered_channel, available_channels)
        self.user_repository.save(user)
        return user

    def list_users(self) -> List[User]:
        """List all users."""
        return self.user_repository.get_all()
