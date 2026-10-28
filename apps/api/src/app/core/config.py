from typing import Literal, Self

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: Literal["development", "test", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    database_url: SecretStr
    redis_url: SecretStr
    storage_endpoint: str
    storage_region: str = "us-east-1"
    storage_access_key: SecretStr
    storage_secret_key: SecretStr
    storage_bucket: str = Field(min_length=3)
    readiness_timeout_s: float = Field(default=3, gt=0, le=30)
    cors_origins: list[str] = []

    @model_validator(mode="after")
    def validate_environment(self) -> Self:
        url = make_url(self.database_url.get_secret_value())
        if url.drivername != "postgresql+asyncpg":
            raise ValueError("DATABASE_URL must use postgresql+asyncpg")
        if self.app_env == "production":
            credentials = (
                url.username or "",
                url.password or "",
                self.storage_access_key.get_secret_value(),
                self.storage_secret_key.get_secret_value(),
            )
            if any("dev" in value.lower() for value in credentials):
                raise ValueError("Development credentials are forbidden in production")
            if not self.storage_endpoint.startswith("https://"):
                raise ValueError("Production storage requires HTTPS")
            if "*" in self.cors_origins:
                raise ValueError("Production CORS requires an explicit allowlist")
        return self
