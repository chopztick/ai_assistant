from app.core.config import get_settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
import logging

# Load settings
settings = get_settings()

# Build connection string
connection_string=f"{settings.database_engine}://{settings.database_user}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Crreate async engine
engine = create_async_engine(
    url=connection_string,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    echo=True
)

# Create async session
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get a session for the database
    """
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logging.error(f"Error in session: {e}")
            raise