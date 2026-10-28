import json

import pytest
from app.core.config import Settings
from app.core.dependencies import DependencyStatus
from app.main import create_app
from fastapi import HTTPException
from fastapi.testclient import TestClient


def test_health_is_liveness_without_infrastructure(settings: Settings) -> None:
    with TestClient(create_app(settings)) as client:
        response = client.get("/health", headers={"X-Correlation-ID": "test-123"})
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["X-Correlation-ID"] == "test-123"


@pytest.mark.parametrize("value", ["a" * 129, "invalid id", "token?secret"])
def test_invalid_correlation_id_is_replaced(settings: Settings, value: str) -> None:
    with TestClient(create_app(settings)) as client:
        response = client.get("/health", headers={"X-Correlation-ID": value})
    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] != value
    assert len(response.headers["X-Correlation-ID"]) == 36


def test_error_contract_for_unknown_route(settings: Settings) -> None:
    with TestClient(create_app(settings)) as client:
        response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert response.json() == {
        "type": "not_found",
        "title": "Request failed",
        "status": 404,
        "detail": "The request could not be completed",
        "code": "NOT_FOUND",
        "correlation_id": response.headers["X-Correlation-ID"],
    }


def test_unhandled_exception_is_sanitized_and_correlated(settings: Settings) -> None:
    app = create_app(settings)

    @app.get("/test-failure")
    async def fail() -> None:
        raise RuntimeError("secret-internals")

    with TestClient(app) as client:
        response = client.get("/test-failure", headers={"X-Correlation-ID": "error-test"})
    assert response.status_code == 500
    assert response.json()["code"] == "INTERNAL_ERROR"
    assert response.headers["X-Correlation-ID"] == "error-test"
    assert "secret-internals" not in response.text


def test_validation_does_not_echo_input(settings: Settings) -> None:
    app = create_app(settings)

    @app.get("/validate")
    async def validate(count: int) -> int:
        return count

    with TestClient(app) as client:
        response = client.get("/validate?count=password-secret")
    assert response.status_code == 422
    assert response.json()["errors"] == [{"field": "query.count", "message": "Invalid value"}]
    assert "password-secret" not in response.text


@pytest.mark.parametrize("status", [401, 403, 409, 429, 501])
def test_http_errors_use_problem_format(settings: Settings, status: int) -> None:
    app = create_app(settings)

    @app.get("/denied")
    async def denied() -> None:
        raise HTTPException(status_code=status, detail="internal-detail")

    with TestClient(app) as client:
        response = client.get("/denied")
    assert response.status_code == status
    assert response.json()["correlation_id"] == response.headers["X-Correlation-ID"]
    assert "internal-detail" not in response.text


@pytest.mark.parametrize("failed", [None, "database", "redis", "storage"])
def test_readiness_status_and_problem_format(settings: Settings, failed: str | None) -> None:
    async def check() -> dict[str, DependencyStatus]:
        return {
            name: "down" if name == failed else "up" for name in ("database", "redis", "storage")
        }

    with TestClient(create_app(settings, readiness_check=check)) as client:
        response = client.get("/ready")
    assert response.status_code == (503 if failed else 200)
    if failed:
        assert response.json()["code"] == "DEPENDENCY_UNAVAILABLE"
    else:
        assert response.json()["dependencies"] == {"database": "up", "redis": "up", "storage": "up"}


def test_structured_request_logs_do_not_include_secrets(
    settings: Settings, capsys: pytest.CaptureFixture[str]
) -> None:
    with TestClient(create_app(settings)) as client:
        client.get(
            "/health?latitude=12.345&ticket=secret",
            headers={
                "Authorization": "Bearer token-secret",
                "X-Correlation-ID": "safe-id",
            },
        )
    log = capsys.readouterr().err
    events = [json.loads(line) for line in log.splitlines() if line.startswith("{")]
    assert any(event.get("correlation_id") == "safe-id" for event in events)
    assert "12.345" not in log
    assert "token-secret" not in log
    assert "ticket=secret" not in log
