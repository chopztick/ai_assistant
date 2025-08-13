from app.core.config import get_settings
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams, Distance

# Load settings
settings = get_settings()

# Get client URL and API key from settings
client_url = settings.vector_db_url
client_api_key = settings.vector_db_api_key

async def get_vector_database_client() -> AsyncQdrantClient:
    """
    Dependency to get a Qdrant client for the vector database
    """
    # Create an instance of AsyncQdrantClient
    qdrant_client = AsyncQdrantClient(url=client_url, api_key=client_api_key)

    if not qdrant_client.collection_exists("test_collection"):
        await qdrant_client.create_collection(
            collection_name="test_collection",
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
        )

    return qdrant_client