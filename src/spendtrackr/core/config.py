# src/spendtrackr/core/config.py

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    app_name: str = "SpendTrackr"
    debug: bool = True

    # DB (MySQL)
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    # Redis
    redis_url: str

    # Auth
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def sqlalchemy_database_uri(self) -> str:
        # mysql+pymysql://user:pass@host:port/db
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
