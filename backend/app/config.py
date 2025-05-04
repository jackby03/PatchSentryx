from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Base Settings loaded from environment variables.
    """

    # Application settings
    APP_NAME: str = "PathSentryx Backend"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "default_secrete_key_change_me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/sample_db"

    # RabbitMQ settings
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"

    # Define model config to load from .env file
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Cache the settings object to avoid reloading it multiple times
@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
