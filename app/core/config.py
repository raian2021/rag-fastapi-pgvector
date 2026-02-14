from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "RAG FastAPI pgvector"
    api_key: str = "change-me"

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "ragdb"
    db_user: str = "raguser"
    db_password: str = "ragpass"

    embed_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    top_k: int = 5
    chunk_size: int = 900
    chunk_overlap: int = 150

settings = Settings()

