from dataclasses import dataclass
from uuid import UUID

@dataclass
class Metadata:
    """
    Metadata class for vector database models.
    This class is used to define the metadata for vector database models.
    """
    id: UUID
    text: str
    description: str
    source_file: str
    source_type: str
    source_location: str
    language: str
    version: str
    chunk_index: int
    tags: list[str]
    created_at: str
    updated_at: str
    embedding_model: str