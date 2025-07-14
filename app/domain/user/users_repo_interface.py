from abc import ABC, abstractmethod
from app.infrastructure.db.models.user import User

class UsersInterface(ABC):
    """
    Repository for managing user-related database operations.
    """
    @abstractmethod
    async def get_user_by_id(self, id: int) -> User:
        """
        Retrieve a user by their ID.
        """
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User:
        """
        Retrieve a user by their email.
        """
        pass

    @abstractmethod
    async def create_user(self, user_data: User) -> User:
        """
        Create a new user.
        """
        pass

    @abstractmethod
    async def update_user(self, id: int, user_data: User) -> User:
        """
        Update an existing user.
        """
        pass

    @abstractmethod
    async def delete_user(self, id: int) -> None:
        """
        Delete a user by their ID.
        """
        pass