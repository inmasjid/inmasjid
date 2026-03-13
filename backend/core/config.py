import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: Literal["local", "prod"] = "local"
    DATABASE_URL: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    OTP_STATIC_PEPPER: str
    MOBILE_ENCRYPTION_KEY: str

    model_config = SettingsConfigDict(env_file_encoding="utf-8")


@lru_cache
def load_settings() -> Settings:
    app_env = os.environ.get("APP_ENV", "local")
    return Settings.model_construct(
        _env_file=Path(f".env.{app_env}"),
        _env_file_encoding="utf-8"
    )


settings = load_settings()
