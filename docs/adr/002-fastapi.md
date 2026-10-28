# ADR-002: FastAPI and typed async Python

Status: accepted in DECISIONS.md.

## Context

The platform needs explicit request/response validation, generated mobile/web contracts and concurrent database/network I/O. Python supports the planned geospatial and reporting ecosystem.

## Decision

Use Python 3.13, FastAPI, Pydantic v2, SQLAlchemy 2 async, asyncpg and Alembic. Explicit Pydantic schemas define responses; ORM models never cross the transport boundary. FastAPI OpenAPI is authoritative. Use strict Pyright and Ruff.

## Alternatives

Django offers integrated administration but would change the chosen API and async persistence architecture. A TypeScript server could share a language with clients but would not remove the need for server-owned domain validation or geospatial processing boundaries.

## Consequences

OpenAPI generation reduces contract drift. Async endpoints must not run CPU-bound parsing, image processing or synchronous SDK calls inline. Third-party typing gaps require narrow stubs with documented surfaces. Pinned dependencies must be installed and checked before the bootstrap is considered verified.
