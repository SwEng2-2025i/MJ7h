class UserAlreadyExistsException(Exception):
    """Exception raised when a user already exists."""

    def __init__(self, message: str = "User already exists."):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(Exception):
    """Exception raised when a user is not found."""

    def __init__(self, message: str = "User not found."):
        self.message = message
        super().__init__(self.message)


class NotificationChainFailedException(Exception):
    """Exception raised when notification chain fails."""

    def __init__(self, message: str = "Notification chain failed."):
        self.message = message
        super().__init__(self.message)
