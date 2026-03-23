"""Application configuration."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "AI Quant Backend"
    version: str = "0.1.0"
    debug: bool = False


settings = Settings()
