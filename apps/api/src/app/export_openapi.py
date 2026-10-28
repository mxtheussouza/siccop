import json

from pydantic import SecretStr

from app.core.config import Settings
from app.main import create_app


def main() -> None:
    # Schema generation is offline: no dependency connections or deployment secrets required.
    # model_validate bypasses environment sources, so local .env values never leak into the schema.
    settings = Settings.model_validate(
        {
            "app_env": "test",
            "database_url": SecretStr("postgresql+asyncpg://schema:schema@localhost/schema"),
            "redis_url": SecretStr("redis://localhost:6379/0"),
            "storage_endpoint": "http://localhost:9000",
            "storage_access_key": SecretStr("schema"),
            "storage_secret_key": SecretStr("schema"),
            "storage_bucket": "schema",
        }
    )
    print(json.dumps(create_app(settings).openapi(), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
