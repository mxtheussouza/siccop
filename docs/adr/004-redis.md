# ADR-004: Redis for durable event windows and ephemeral state

Status: accepted in DECISIONS.md.

## Context

Multiple API processes must share replayable operation events, rate limits, current tracking hints and short-lived WebSocket tickets. Durable business state remains in PostgreSQL.

## Decision

Use Redis. Later durable events use capped Streams per operation and a sequence counter. Ephemeral location updates use separate capped transport/state and reconnecting clients obtain a current snapshot. Never treat Pub/Sub as a durable event log.

## Alternatives

Pub/Sub has less bookkeeping but loses messages for disconnected clients. Kafka has stronger log-oriented tooling but adds operational complexity beyond v1 needs. Process-local caches break cross-instance coordination.

## Consequences

Redis availability is part of readiness. Stream retention bounds catch-up; clients must handle resynchronization. Redis persistence does not replace the transactional PostgreSQL outbox. Phase 01 provides Redis infrastructure and a real readiness probe; events and rate limits are future phases.
