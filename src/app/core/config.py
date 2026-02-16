from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    EMBEDDING_URL: str = "fill_with_real_value"

    QDRANT_HOST: str = "fill_with_real_value"
    QDRANT_PORT: int = 6333

    # LLM_URL: str = "fill_with_real_value"
    # LLM_TOKEN: str = "fill_with_real_value"

    COLLECTION_NAME: str = "test"
    DEFAULT_COLLECTION: str = "test"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200


settings = Settings()
