from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    API_VERSION: str
    CHROMA_DB_PATH: str
    MODEL_NAME: str
    EMBEDDING_MODEL: str

    class Config:
        env_file = ".env"


settings = Settings()