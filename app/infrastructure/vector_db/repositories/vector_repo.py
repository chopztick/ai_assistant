from qdrant_client import AsyncQdrantClient
from app.domain.vector.vector_repo_interface import VectorDatabaseInterface


class VectorDbRepository(VectorDatabaseInterface):
    """
    Repository for managing vector database operations.
    This class implements the VectorDatabaseInterface and provides methods
    to add, retrieve, and delete vectors from the database.
    """

    def __init__(self, vector_db_client: AsyncQdrantClient):
        self.vector_db_client = vector_db_client

    async def add_vector(self, vector: list, metadata: dict) -> str:
        raise NotImplementedError

    async def vector_search(self, vector_id: str) -> dict:
        raise NotImplementedError

    async def delete_vector(self, vector_id: str) -> bool:
        raise NotImplementedError