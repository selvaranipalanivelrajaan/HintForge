from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "examate-rag"
    environment: str = "local"  # local | ci | production

    # LLM providers (both are OpenAI-compatible APIs)
    groq_api_key: str = ""
    gemini_api_key: str = ""
    primary_model: str = "llama-3.3-70b-versatile"  # used with Groq
    gemini_model: str = "gemini-3.6-flash"
    fallback_model: str = "gemini-3.5-flash-lite"


@lru_cache
def get_settings() -> Settings:
    return Settings()
