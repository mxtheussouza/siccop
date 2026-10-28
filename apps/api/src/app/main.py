from collections.abc import Awaitable, Callable
from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.core.config import Settings, load_settings
from app.core.dependencies import DependencyProbe, DependencyStatus
from app.core.errors import ApplicationError, ProblemRead, register_error_handlers
from app.core.logging import configure_logging
from app.core.middleware import CorrelationMiddleware

ReadinessCheck = Callable[[], Awaitable[dict[str, DependencyStatus]]]


class HealthRead(BaseModel):
    status: Literal["ok"] = "ok"


class ReadyRead(BaseModel):
    status: Literal["ready"] = "ready"
    dependencies: dict[str, DependencyStatus]


def create_app(
    settings: Settings | None = None, readiness_check: ReadinessCheck | None = None
) -> FastAPI:
    config = settings or load_settings()
    configure_logging(config.log_level)
    app = FastAPI(
        title="Operational Platform API",
        version="0.1.0",
        debug=False,
        docs_url=None if config.app_env == "production" else "/docs",
        redoc_url=None,
        responses={422: {"model": ProblemRead}, 500: {"model": ProblemRead}},
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["X-Correlation-ID", "Content-Type"],
        expose_headers=["X-Correlation-ID"],
    )
    app.add_middleware(CorrelationMiddleware)
    register_error_handlers(app)
    check = readiness_check or DependencyProbe(config).check

    async def health() -> HealthRead:
        return HealthRead()

    async def ready() -> ReadyRead:
        statuses = await check()
        if set(statuses) != {"database", "redis", "storage"} or any(
            value != "up" for value in statuses.values()
        ):
            raise ApplicationError(
                status=503,
                code="DEPENDENCY_UNAVAILABLE",
                title="Not ready",
                detail="A required dependency is unavailable",
            )
        return ReadyRead(dependencies=statuses)

    app.get("/health", response_model=HealthRead, operation_id="get_health", tags=["platform"])(
        health
    )
    app.get(
        "/ready",
        response_model=ReadyRead,
        operation_id="get_readiness",
        tags=["platform"],
        responses={503: {"model": ProblemRead}},
    )(ready)
    return app
