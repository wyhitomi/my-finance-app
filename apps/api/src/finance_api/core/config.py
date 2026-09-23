from functools import lru_cache
from importlib.metadata import version
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, read from environment variables prefixed with FINANCE_."""

    model_config = SettingsConfigDict(env_prefix="FINANCE_", env_file=".env", extra="ignore")

    app_name: str = "My Finance API"
    version: str = version("finance-api")
    environment: Literal["development", "test", "staging", "production"] = "development"
    cors_origins: list[str] = ["http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
