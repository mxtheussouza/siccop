# ADR-008: Dramatiq background worker

Status: accepted in DECISIONS.md.

## Context

Thumbnails, HEIC conversion, XML/archive parsing, large PDF reports and retention must not block the API event loop. Failures need bounded retry and observability.

## Decision

Use Dramatiq with a Redis broker. Job payloads reference authorized persisted work rather than embedding sensitive URLs or large binary data. Actors must be idempotent because delivery and retries can repeat work. Domain jobs are introduced in their owning phases.

## Alternatives

Celery has a broader workflow ecosystem but more configuration than required for these jobs. FastAPI background tasks share API process lifetime and do not provide durable delivery. Direct inline execution increases latency and blocks concurrent I/O when work is synchronous.

## Consequences

Workers become an additional deployment process with health and error monitoring. Retries are not a substitute for validating input or transactional state transitions. The Phase 01 worker has a configured broker and no fake processing actors; actual attachment jobs start in Phase 06.
