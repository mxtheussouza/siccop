import pytest
from app.core.config import Settings
from pydantic import SecretStr


@pytest.fixture
def settings() -> Settings:
    return Settings(
        _env_file=None,
        app_env="test",
        database_url=SecretStr("postgresql+asyncpg://test:test@localhost/test"),
        redis_url=SecretStr("redis://localhost:6379/0"),
        storage_endpoint="http://localhost:9000",
        storage_access_key=SecretStr("test-key"),
        storage_secret_key=SecretStr("test-secret"),
        storage_bucket="test-bucket",
        cors_origins=[],
    )
