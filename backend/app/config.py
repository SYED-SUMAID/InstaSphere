from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):

    DATABASE_URL: str = "postgresql+psycopg://postgres:your_password@localhost:5432/instasphere"

    SECRET_KEY: str = "replace-this-with-a-secure-secret-key"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()