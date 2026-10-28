import re
from uuid import uuid4

import structlog
from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.errors import ApplicationError, problem_response

CORRELATION_ID = re.compile(r"^[A-Za-z0-9._-]{1,128}$")
logger = structlog.get_logger()


class CorrelationMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        request = Request(scope)
        incoming = request.headers.get("X-Correlation-ID", "")
        correlation_id = incoming if CORRELATION_ID.fullmatch(incoming) else str(uuid4())
        request.state.correlation_id = correlation_id
        tokens = structlog.contextvars.bind_contextvars(correlation_id=correlation_id)
        started = False

        async def send_with_headers(message: Message) -> None:
            nonlocal started
            if message["type"] == "http.response.start":
                started = True
                headers = list(message.get("headers", []))
                headers.append((b"x-correlation-id", correlation_id.encode("ascii")))
                message["headers"] = headers
                logger.info("http_request", method=request.method, status=message["status"])
            await send(message)

        try:
            await self.app(scope, receive, send_with_headers)
        except Exception:
            # No exception text, request paths, query strings, bodies or headers in logs.
            logger.error("unhandled_request_error")
            if started:
                raise
            response = problem_response(
                request,
                ApplicationError(
                    status=500,
                    code="INTERNAL_ERROR",
                    title="Internal error",
                    detail="The request could not be completed",
                ),
            )
            await response(scope, receive, send_with_headers)
        finally:
            structlog.contextvars.reset_contextvars(**tokens)
