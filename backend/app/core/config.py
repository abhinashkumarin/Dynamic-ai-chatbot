"""Application Configuration — loads from .env"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 🔥 IMPORTANT: ensure .env load ho
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


class Settings(BaseSettings):
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # MongoDB
     # MongoDB (❗ default blank rakho, localhost hatao)
    MONGODB_URL: str
    DATABASE_NAME: str = "ai_chatbot_db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_TTL: int = 300

    # JWT
    SECRET_KEY: str = "change_me_in_production_use_32_char_min"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    # OpenAI (optional)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"

    # NLP
    CONFIDENCE_THRESHOLD: float = 0.65
    MAX_HISTORY_TURNS: int = 20
    MODEL_PATH: str = "app/training/saved_models"

    # Features
    ENABLE_ANALYTICS: bool = True
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
