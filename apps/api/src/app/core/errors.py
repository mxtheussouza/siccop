from typing import Literal

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

ErrorType = Literal[
    "validation",
    "unauthorized",
    "forbidden",
    "not_found",
    "conflict",
    "rate_limited",
    "not_implemented",
    "internal",
]
ErrorCode = Literal[
    "VALIDATION_ERROR",
    "UNAUTHORIZED",
    "FORBIDDEN",
    "NOT_FOUND",
    "CONFLICT",
    "RATE_LIMITED",
    "NOT_IMPLEMENTED",
    "INTERNAL_ERROR",
    "DEPENDENCY_UNAVAILABLE",
    "HTTP_ERROR",
]


class FieldError(BaseModel):
    field: str
    message: str


class ProblemRead(BaseModel):
    type: ErrorType
    title: str
    status: int
    detail: str
    code: ErrorCode
    correlation_id: str
    errors: list[FieldError] | None = None


class ApplicationError(Exception):
    status: int
    code: ErrorCode
    title: str
    detail: str
    error_type: ErrorType

    def __init__(
        self,
        *,
        status: int,
        code: ErrorCode,
        title: str,
        detail: str,
        error_type: ErrorType = "internal",
    ) -> None:
        super().__init__(code)
        self.status = status
        self.code = code
        self.title = title
        self.detail = detail
        self.error_type = error_type


def problem_response(
    request: Request, error: ApplicationError, fields: list[FieldError] | None = None
) -> JSONResponse:
    body = ProblemRead(
        type=error.error_type,
        title=error.title,
        status=error.status,
        detail=error.detail,
        code=error.code,
        correlation_id=request.state.correlation_id,
        errors=fields,
    )
    return JSONResponse(status_code=error.status, content=body.model_dump(exclude_none=True))


def register_error_handlers(app: FastAPI) -> None:
    async def handle_application(request: Request, error: ApplicationError) -> JSONResponse:
        return problem_response(request, error)

    async def handle_validation(request: Request, error: RequestValidationError) -> JSONResponse:
        # Never echo inputs or parser context (passwords/tokens/coordinates may be present).
        fields = [
            FieldError(field=".".join(str(part) for part in item["loc"]), message="Invalid value")
            for item in error.errors()
        ]
        return problem_response(
            request,
            ApplicationError(
                status=422,
                code="VALIDATION_ERROR",
                title="Validation failed",
                detail="One or more fields are invalid",
                error_type="validation",
            ),
            fields,
        )

    async def handle_http(request: Request, error: HTTPException) -> JSONResponse:
        types: dict[int, tuple[ErrorType, ErrorCode]] = {
            401: ("unauthorized", "UNAUTHORIZED"),
            403: ("forbidden", "FORBIDDEN"),
            404: ("not_found", "NOT_FOUND"),
            409: ("conflict", "CONFLICT"),
            422: ("validation", "VALIDATION_ERROR"),
            429: ("rate_limited", "RATE_LIMITED"),
            501: ("not_implemented", "NOT_IMPLEMENTED"),
        }
        kind, code = types.get(error.status_code, ("internal", "HTTP_ERROR"))
        return problem_response(
            request,
            ApplicationError(
                status=error.status_code,
                code=code,
                title="Request failed",
                detail="The request could not be completed",
                error_type=kind,
            ),
        )

    app.exception_handler(ApplicationError)(handle_application)
    app.exception_handler(RequestValidationError)(handle_validation)
    app.exception_handler(HTTPException)(handle_http)
