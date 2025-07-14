import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

# Determine the environment name from the environment variable
env_name = os.getenv('ENV_NAME', 'dev').lower()  # DEV, STAGE, PROD, TEST

class Settings(BaseSettings):
    '''
    Settings for the application, loads from .env file based on the environment name
    '''
    environment: str = "Local"
    debug: bool = True
    llm_provider: str = "mistral"
    llm_model: str = "mistral-large-latest"
    llm_api_key: str = "your_mistral_api_key"
    database_engine: str = "postgresql+asyncpg"
    database_user: str = "postgres"
    database_password: str = "postgres"
    database_hostname: str = "localhost"
    database_port: int = 5432
    database_name: str = "postgres"
    vector_db_url: str = "https://your-qdrant-url"
    vector_db_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file= f".env.{env_name}",
        env_file_encoding= 'utf-8'
    )

# Cache the settings to avoid reloading them on every request
@lru_cache()
def get_settings() -> Settings:
    setting = Settings()
    print(f"Loading settings for: {setting.environment}")
    return setting
