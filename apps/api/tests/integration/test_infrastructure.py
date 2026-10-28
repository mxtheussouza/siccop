import asyncio
import os
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

import boto3
import pytest
from app.core.config import Settings
from app.core.dependencies import DependencyProbe
from app.main import create_app
from httpx import ASGITransport, AsyncClient
from pydantic import SecretStr
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def infrastructure() -> Iterator[tuple[Settings, DockerContainer]]:
    with (
        DockerContainer("postgis/postgis:17-3.5")
        .with_env("POSTGRES_USER", "platform_test")
        .with_env("POSTGRES_PASSWORD", "integration-only-password")
        .with_env("POSTGRES_DB", "platform_test")
        .with_exposed_ports(5432) as database,
        DockerContainer("redis:7.4.2-alpine").with_exposed_ports(6379) as redis,
        DockerContainer("minio/minio:RELEASE.2025-04-22T22-12-26Z")
        .with_env("MINIO_ROOT_USER", "integration-key")
        .with_env("MINIO_ROOT_PASSWORD", "integration-secret")
        .with_command("server /data")
        .with_exposed_ports(9000) as storage,
    ):
        wait_for_logs(database, "database system is ready to accept connections")
        wait_for_logs(redis, "Ready to accept connections")
        wait_for_logs(storage, "API:")
        config = Settings(
            _env_file=None,
            app_env="test",
            readiness_timeout_s=1,
            database_url=SecretStr(
                f"postgresql+asyncpg://platform_test:integration-only-password@"
                f"{database.get_container_host_ip()}:{database.get_exposed_port(5432)}/platform_test"
            ),
            redis_url=SecretStr(
                f"redis://{redis.get_container_host_ip()}:{redis.get_exposed_port(6379)}/0"
            ),
            storage_endpoint=f"http://{storage.get_container_host_ip()}:"
            f"{storage.get_exposed_port(9000)}",
            storage_access_key=SecretStr("integration-key"),
            storage_secret_key=SecretStr("integration-secret"),
            storage_bucket="integration-bucket",
        )
        with boto3.client(
            "s3",
            endpoint_url=config.storage_endpoint,
            aws_access_key_id="integration-key",
            aws_secret_access_key="integration-secret",
            region_name="us-east-1",
        ) as client:
            client.create_bucket(Bucket=config.storage_bucket)
        yield config, redis


async def test_postgis_migration_and_readiness_redis_outage(
    infrastructure: tuple[Settings, DockerContainer],
) -> None:
    settings, redis = infrastructure
    probe = DependencyProbe(settings)
    for _ in range(30):
        if all(value == "up" for value in (await probe.check()).values()):
            break
        await asyncio.sleep(0.2)
    else:
        pytest.fail("Real infrastructure did not become ready")
    environment = os.environ | {
        name.upper(): value.get_secret_value() if isinstance(value, SecretStr) else str(value)
        for name, value in settings
        if name != "cors_origins"
    }
    result = await asyncio.to_thread(
        subprocess.run,
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=Path(__file__).resolve().parents[2],
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, "Alembic migration failed; inspect local migration output"
    engine = create_async_engine(settings.database_url.get_secret_value())
    try:
        async with engine.connect() as connection:
            version = await connection.scalar(text("SELECT PostGIS_Version()"))
            assert str(version).startswith("3.5")
            revision = await connection.scalar(text("SELECT version_num FROM alembic_version"))
            assert revision == "0001"
    finally:
        await engine.dispose()
    async with AsyncClient(
        transport=ASGITransport(app=create_app(settings)), base_url="http://test"
    ) as client:
        assert (await client.get("/ready")).status_code == 200
        await asyncio.to_thread(redis.stop)
        response = await client.get("/ready")
        assert response.status_code == 503
        assert response.json()["code"] == "DEPENDENCY_UNAVAILABLE"
        assert (await client.get("/health")).status_code == 200
