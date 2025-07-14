from app.domain.user.users_repo_interface import UsersInterface
from app.infrastructure.db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.user_models import UserUpdate

class UsersRepository(UsersInterface):
    """
    Repository for managing user-related database operations.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the UsersRepository with a database session.

        Args:
            session: The database session to use for operations.
        """
        self.session = session

    async def get_user_by_id(self, id: int) -> User:
        """
        Retrieve a user by their ID.

        Args:
            id: The ID of the user to retrieve.

        Returns:
            User: The user object.
        """
        stmt = select(User).where(User.id == id)
        result = await self.session.execute(stmt)
        return result.scalars().first()
    
    async def get_user_by_email(self, email: str) -> User:
        """
        Retrieve a user by their email.

        Args:
            email: The email of the user to retrieve.

        Returns:
            User: The user object.
        """
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)

        user = result.scalars().one_or_none()

        if user is None:
            raise ValueError(f"User with id {id} not found") 
        
        return user
    
    async def create_user(self, user_data: User) -> User:
        """
        Create a new user.

        Args:
            user_data: The user data to create.

        Returns:
            User: The created user object.
        """
        self.session.add(user_data)
        await self.session.flush()
        return user_data
    
    async def update_user(self, id: int, user_data: UserUpdate) -> User:
        """
        Update an existing user.

        Args:
            id: The ID of the user to update.
            user_data: The new user data.

        Returns:
            User: The updated user object.
        """
        stmt = select(User).where(User.id == id)
        result = await self.session.execute(stmt)

        user = result.scalars().one_or_none()

        if user is None:
            raise ValueError(f"User with id {id} not found")            
        
        user.firstname = user_data.firstname
        user.lastname = user_data.lastname
        user.email = user_data.email

        await self.session.commit()
        await self.session.refresh(user)

        return user
    
    async def delete_user(self, id: int) -> None:
        """
        Delete a user by their ID.

        Args:
            id: The ID of the user to delete.
        """
        stmt = select(User).where(User.id == id)
        result = await self.session.execute(stmt)

        user = result.scalars().one_or_none()

        if user is None:
            raise ValueError(f"User with id {id} not found")            
        
        await self.session.delete(user)
        await self.session.commit()