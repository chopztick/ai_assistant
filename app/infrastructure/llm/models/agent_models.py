from dataclasses import dataclass
from app.infrastructure.db.repositories.users_repo import UsersRepository

@dataclass
class Deps:
    """
    Dependency class for the agent.
    """
    user_repo: UsersRepository = None