from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointStruct
from app.domain.vector.vector_repo_interface import VectorDatabaseInterface
from app.infrastructure.vector_db.models.vector_db_models import Metadata

class VectorDbRepository(VectorDatabaseInterface):
    """
    Repository for managing vector database operations.
    This class implements the VectorDatabaseInterface and provides methods
    to add, retrieve, and delete vectors from the database.
    """

    def __init__(self, vector_db_client: AsyncQdrantClient):
        self.vector_db_client = vector_db_client

    async def add_vector(self, vector: list[float], metadata: Metadata) -> str:
        """
        Adds a vector to the database with associated metadata.
        :param vector: The vector to be added.
        :param metadata: Metadata associated with the vector.
        :return: The ID of the added vector.
        """
        # Upsert the vector with metadata into the "documents" collection
        await self.vector_db_client.upsert(
            collection_name="documents",
            points=[
                PointStruct(
                    id=str(metadata.id),
                    vector=vector,
                    payload={
                        "text": metadata.text,
                        "description": metadata.description,
                        "source_file": metadata.source_file,
                        "source_type": metadata.source_type,
                        "source_location": metadata.source_location,
                        "language": metadata.language,
                        "version": metadata.version,
                        "chunk_index": metadata.chunk_index,
                        "tags": metadata.tags,
                        "created_at": metadata.created_at,
                        "updated_at": metadata.updated_at,
                        "embedding_model": metadata.embedding_model
                    }
                )
            ]
        )

        return str(metadata.id)

    async def vector_search(self, vector_id: str) -> dict:
        raise NotImplementedError

    async def delete_vector(self, vector_id: str) -> bool:
        raise NotImplementedError