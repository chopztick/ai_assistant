from abc import ABC, abstractmethod
from app.infrastructure.vector_db.models.vector_db_models import Metadata

class VectorDatabaseInterface(ABC):
    """
    Interface for vector database operations.
    """

    @abstractmethod
    async def add_vector(self, vector: list[float], metadata: Metadata) -> str:
        """
        Add a vector to the database.

        :param vector: The vector to add.
        :param metadata: Metadata associated with the vector.
        :return: The ID of the added vector.
        """
        pass

    @abstractmethod
    async def vector_search(self, vector_id: str) -> dict:
        """
        Retrieve a vector from the database by its ID.

        :param vector_id: The ID of the vector to retrieve.
        :return: The retrieved vector and its metadata.
        """
        pass

    @abstractmethod
    async def delete_vector(self, vector_id: str) -> bool:
        """
        Delete a vector from the database by its ID.

        :param vector_id: The ID of the vector to delete.
        :return: True if deletion was successful, False otherwise.
        """
        pass