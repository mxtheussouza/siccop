# Phase 04 — Incidents backend

**Objective:** correct, concurrency-safe incident domain: state machine, atomic capture, optimistic locking, assignments, append-only actions. API only.

**Read:** SPEC §4 (Incident*, IncidentType), §5 (Incident state machine, Capture), §6 (INC-01..07), §3; DECISIONS (Errors, Offline command table for idempotency expectations).

## Tasks

1. Migrations: `incident_types`, `incidents` (PostGIS `Point(4326)`, GiST index, partial indexes for open incidents, `version`, per-operation reference-number sequence), `incident_transitions`, `incident_assignments`, `incident_actions`. Check constraints on status/priority; DB-level guard that actions/transitions are append-only (no UPDATE/DELETE grants).
2. Domain: pure state machine (`domain/`) with the table from SPEC §5, min-role and reason rules; no I/O.
3. Application services with explicit unit-of-work transactions: create, update (`If-Match`/`version`), transition, claim/release, assign/unassign (team/agent; recorded in `incident_assignments`; status change in the same transaction), register action, list (cursor pagination, filters: type, priority, status, assignment, bbox, text), get with timeline.
4. Claim implementation: single conditional `UPDATE … WHERE claimed_by IS NULL … RETURNING` (or `SELECT … FOR UPDATE`) — exactly one winner. Losers → 409 `INCIDENT_ALREADY_CLAIMED`.
5. Domain events written to `domain_event_outbox` in the same transaction for: `incident.created|updated|assigned|status.changed|claimed|released|action.created` (relay is Phase 05).
6. Audit events for transitions and assignments (no coordinates in metadata).
7. Idempotency: create/action/transition accept `Idempotency-Key`; create is also idempotent by client-supplied `id`.
8. Endpoints under `/api/v1/operations/{operation_id}/incidents…` + incident types. Schemas `IncidentCreate|Update|Read|ListItem`. Regenerate contracts.
9. Seed: incident types and incidents in several states.

## Tests (real PostgreSQL)

- State machine: every allowed transition, every disallowed pair (table-driven), role and reason rules, reopen, terminal states.
- **Concurrency: ≥ 20 parallel claim requests → exactly 1×2xx and 19×409** (repeat 20 times for flakiness).
- Optimistic locking: concurrent PATCHes with the same version → one wins, other 409 `VERSION_CONFLICT`.
- Assignment + transition atomicity (force a failure mid-transaction → nothing persisted).
- Append-only enforcement at DB level.
- Authz matrix rows for all incident endpoints; operation isolation.
- Pagination correctness (no duplicates/gaps under inserts); query-count assertion on list (no N+1).
- Idempotent replay of create/action.

## Exit criteria

- `make verify` green; coverage on `incidents` ≥ 90 %.
- INC-01..07 updated in PROGRESS with test names; SCENARIO 8 evidence recorded.
- EXPLAIN shows index use for bbox query and open-incident list (assert in test).

## Out of scope

Realtime delivery, attachments, UI.
