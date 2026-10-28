import pytest
from app.core.config import Settings
from pydantic import ValidationError


def test_settings_load_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    values = {
        "APP_ENV": "test",
        "DATABASE_URL": "postgresql+asyncpg://test:test@localhost/test",
        "REDIS_URL": "redis://localhost:6379/1",
        "STORAGE_ENDPOINT": "http://localhost:9000",
        "STORAGE_ACCESS_KEY": "test",
        "STORAGE_SECRET_KEY": "test-password",
        "STORAGE_BUCKET": "test-bucket",
        "CORS_ORIGINS": '["http://localhost:3000"]',
    }
    for name, value in values.items():
        monkeypatch.setenv(name, value)
    config = Settings(_env_file=None)
    assert config.app_env == "test"
    assert config.cors_origins == ["http://localhost:3000"]
    assert "test-password" not in repr(config)


def test_sqlite_is_rejected(settings: Settings) -> None:
    with pytest.raises(ValidationError, match="postgresql\\+asyncpg"):
        Settings(**(settings.model_dump() | {"database_url": "sqlite:///test.db"}))


def test_production_rejects_development_credentials(settings: Settings) -> None:
    with pytest.raises(ValidationError, match="Development credentials"):
        Settings(
            **(
                settings.model_dump()
                | {
                    "app_env": "production",
                    "storage_access_key": "platform-dev",
                    "storage_endpoint": "https://storage.example.com",
                }
            )
        )
