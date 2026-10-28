import logging

import structlog
from structlog.types import EventDict


def ensure_correlation_id(_logger: object, _method: str, event: EventDict) -> EventDict:
    # Startup and worker infrastructure logs have no HTTP request context.
    event.setdefault("correlation_id", "system")
    return event


def configure_logging(level: str) -> None:
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
        ],
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            ensure_correlation_id,
            structlog.processors.JSONRenderer(),
        ],
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.basicConfig(level=level, handlers=[handler], force=True)
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        managed = logging.getLogger(name)
        managed.handlers.clear()
        managed.propagate = True
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            ensure_correlation_id,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelNamesMapping()[level]),
        cache_logger_on_first_use=True,
    )
    # Third-party HTTP debug logging can expose signed URLs or credentials.
    for name in ("httpx", "httpcore", "botocore", "boto3", "sqlalchemy.engine"):
        logging.getLogger(name).setLevel(logging.WARNING)
