import asyncio
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Literal

import anyio
import boto3
import structlog
from botocore.config import Config
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import Settings

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client  # Development-only stubs package.

DependencyStatus = Literal["up", "down"]
logger = structlog.get_logger()


class DependencyProbe:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def database(self) -> None:
        engine = create_async_engine(
            self.settings.database_url.get_secret_value(), pool_pre_ping=True, hide_parameters=True
        )
        try:
            async with engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
        finally:
            await engine.dispose()

    async def redis(self) -> None:
        # redis-py 5 leaves **kwargs untyped; arguments here are explicit and typed by Settings.
        client = Redis.from_url(  # pyright: ignore[reportUnknownMemberType]
            self.settings.redis_url.get_secret_value(),
            socket_timeout=self.settings.readiness_timeout_s,
        )
        try:
            # redis-py 5 types ping as Awaitable[Any] | Any; the asyncio client always awaits.
            await client.ping()  # pyright: ignore[reportUnknownMemberType]
        finally:
            await client.aclose()

    async def storage(self) -> None:
        def head_bucket() -> None:
            # boto3-stubs only ships the S3 overload here; other service overloads are Unknown.
            client: S3Client = boto3.session.Session().client(  # pyright: ignore[reportUnknownMemberType]
                "s3",
                endpoint_url=self.settings.storage_endpoint,
                aws_access_key_id=self.settings.storage_access_key.get_secret_value(),
                aws_secret_access_key=self.settings.storage_secret_key.get_secret_value(),
                region_name=self.settings.storage_region,
                config=Config(
                    connect_timeout=self.settings.readiness_timeout_s,
                    read_timeout=self.settings.readiness_timeout_s,
                    retries={"max_attempts": 0},
                    s3={"addressing_style": "path"},
                ),
            )
            try:
                client.head_bucket(Bucket=self.settings.storage_bucket)
            finally:
                client.close()

        await anyio.to_thread.run_sync(head_bucket, abandon_on_cancel=True)

    async def check(self) -> dict[str, DependencyStatus]:
        async def run(name: str, check: Callable[[], Awaitable[None]]) -> DependencyStatus:
            try:
                async with asyncio.timeout(self.settings.readiness_timeout_s):
                    await check()
                return "up"
            except Exception:
                logger.warning("readiness_dependency_unavailable", dependency=name)
                return "down"

        checks = {"database": self.database, "redis": self.redis, "storage": self.storage}
        # Resources are created per probe and always closed; no clients are shared across loops.
        statuses = await asyncio.gather(*(run(name, check) for name, check in checks.items()))
        return dict(zip(checks, statuses, strict=True))
