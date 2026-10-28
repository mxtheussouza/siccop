# ADR-006: Mobile offline command outbox

Status: accepted in DECISIONS.md.

## Context

Field connectivity may disappear after a user creates an incident or action. Replaying arbitrary writes can duplicate records or overwrite later server decisions.

## Decision

Use SQLite for cached data and a persistent, ordered command outbox per operation. Only the command types listed in DECISIONS.md may be created offline. Use dependencies, stable client IDs and idempotency keys. Keep location fixes in a separate write-ahead buffer. The server validates all transitions and remains authoritative.

## Alternatives

Memory queues lose commands when the app is terminated. Generic last-write-wins synchronization hides operational conflicts. Requiring connectivity for every action reduces implementation work but fails the stated field workflow.

## Consequences

Retries need backoff and jitter; permanent failures need user-visible retry/edit/discard controls. Dependent discards require confirmation. SQLite counts drive sync status. Phase 10 implements persistence and reconciliation; the Phase 01 mobile tabs do not claim offline support.
