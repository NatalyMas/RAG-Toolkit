from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    EMBEDDING_URL: str = "http://gpt-dev.igatec.com:8000"

    QDRANT_HOST: str = "http://gpt-dev.igatec.com"
    QDRANT_PORT: int = 6333

    # LLM_URL: str = "https://gpt-dev.igatec.com/"
    # LLM_TOKEN: str = "RWD6B0D-PM54KDA-KQ283A8-GQECS6Z"

    COLLECTION_NAME: str = "test"
    DEFAULT_COLLECTION: str = "test"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200


settings = Settings()
