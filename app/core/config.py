from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.core.constants import LDS
import os



BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    APP_NAME: str = "Akio"

    DATABASE_URL: str = "sqlite+aiosqlite:///./akio.db"

    LDS_BASE_URL: str = LDS.BASE_URL

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()