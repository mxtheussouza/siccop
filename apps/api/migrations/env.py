import asyncio
from pathlib import Path

from alembic import context
from app.core.config import Settings
from sqlalchemy import Connection, pool
from sqlalchemy.ext.asyncio import create_async_engine

target_metadata = None
settings = Settings(_env_file=Path(__file__).resolve().parents[3] / ".env")


def run_sync_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_online() -> None:
    engine = create_async_engine(
        settings.database_url.get_secret_value(), poolclass=pool.NullPool, hide_parameters=True
    )
    try:
        async with engine.connect() as connection:
            await connection.run_sync(run_sync_migrations)
    finally:
        await engine.dispose()


if context.is_offline_mode():
    context.configure(
        url=settings.database_url.get_secret_value(),
        literal_binds=True,
        target_metadata=target_metadata,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()
else:
    asyncio.run(run_online())
