from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env")

    APP_NAME: str
    APP_VERSION: str
    GROQ_API_KEY: str
    APP_ENV: str
    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE_MB: int
    FILE_DEFAULT_CHUNK_SIZE: int


@lru_cache()
def get_settings() -> Settings:
    return Settings()
