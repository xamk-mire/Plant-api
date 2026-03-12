from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://plantuser:plantpass@localhost:5433/plant_mock_db"
    api_key_header: str = "X-API-Key"
    secret_key: str | None = None
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
