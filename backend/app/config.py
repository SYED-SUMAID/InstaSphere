from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str = "postgresql+psycopg://postgres:your_password@localhost:5432/instasphere"

    SECRET_KEY: str = "replace-with-your-generated-secret-key"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()