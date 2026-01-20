"""Application settings.

Centralized configuration loaded from environment variables.
"""

from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment."""
    
    # Application
    app_name: str = "SomaAI"
    version: str = "0.1.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./somaai.db"
    
    # Redis / Cache
    redis_url: str = "redis://localhost:6379/0"
    redis_password: Optional[str] = None
    
    # Vector Database (Qdrant)
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "somaai_documents"
    
    # Storage
    storage_backend: str = "local"  # local | gdrive
    storage_local_path: str = "./uploads"
    gdrive_credentials_path: Optional[str] = None
    gdrive_folder_id: Optional[str] = None
    
    # Background Jobs
    queue_backend: str = "redis"  # redis | sync
    
    # Cache TTLs (seconds)
    cache_query_ttl: int = 86400
    cache_embedding_ttl: int = 604800
    cache_retrieval_ttl: int = 3600
    cache_session_ttl: int = 3600
    
    # Semantic Cache
    cache_semantic_enabled: bool = True
    cache_similarity_threshold: float = 0.92
    cache_embedding_dim: int = 768
    cache_namespace: str = "somaai"
    
    # LLM Provider
    llm_provider: str = "openai"  # openai | anthropic | huggingface
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
