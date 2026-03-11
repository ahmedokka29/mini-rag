from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    GROQ_API_KEY: str

    class Config:
        env_file = ".env"
