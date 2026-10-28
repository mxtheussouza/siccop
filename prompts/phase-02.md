# Phase 02 — Identity, hierarchy, operations, RBAC, audit foundation

**Objective:** authenticated, authorized, operation-scoped API with an append-only audit trail. Everything later depends on this being correct.

**Read:** SPEC §2, §3, §4 (User…OperationMembership, AuditEvent, IdempotencyRecord), §6 (AUTH, AUTHZ, ADM, OPS, AUD-01); DECISIONS (Authentication topology, Errors, Backend stack).

## Tasks

1. Alembic migrations: users, user_identity (OIDC-ready), refresh_tokens (family model), organizations, command_centers, operations, operation_memberships, audit_events (revoke UPDATE/DELETE from the app DB role), idempotency_records, domain_event_outbox (table only; relay comes in Phase 05). Constraints, indexes, check constraints.
2. `identity`: login, logout, refresh with rotation + reuse detection, password change, enable/disable, `token_version`, Argon2id, login/refresh rate limiting (Redis), generic auth errors, cookie handling for web and body handling for `X-Client: mobile`, Origin/Host check on cookie endpoints.
3. `organizations`, `command_centers`, `operations` (lifecycle state machine), memberships: full CRUD for ADMINISTRATOR.
4. Policy layer: one dependency (`require(operation_id, permission)`) implementing the SPEC §3 matrix. Operation-status write rule (ACTIVE only). No role checks outside this layer.
5. Idempotency middleware/dependency (`Idempotency-Key`), 7-day TTL, request-hash mismatch → 422 `IDEMPOTENCY_KEY_REUSED`.
6. Audit service (append-only) used by identity and admin flows: login/logout, role changes, config changes, operation lifecycle. Correlation ID stored.
7. Dev seed (users for each role, org, command center, ACTIVE operation) — refuses to run when `APP_ENV=production`.
8. Update OpenAPI + generated TS contracts.

## Tests (real PostgreSQL via Testcontainers)

- Auth: login ok/bad password/disabled user; refresh rotation; **reuse of an old refresh token revokes the family**; password change revokes sessions; rate limit triggers; error bodies match the format.
- **Table-driven authorization test covering every cell of the SPEC §3 matrix** for all endpoints that exist now.
- Isolation: user with membership in operation A gets 403 on operation B for every operation-scoped endpoint.
- Memberships: same user CHIEF in A and OBSERVER in B behaves correctly.
- Audit rows are created and cannot be updated/deleted by the app role (assert DB error).
- Idempotent replay returns identical response and creates one row.

## Exit criteria

- `make verify` green; backend coverage on `identity` and policy layer ≥ 90 %.
- Requirements AUTH-01..04, AUTHZ-01..03, ADM-01..05, OPS-01 (API part), AUD-01 (identity/admin events) updated in PROGRESS with test names.
- Seed works (`make migrate seed`) and a manual `curl` login with the seed admin returns tokens (paste evidence).

## Out of scope

Web/mobile UI, realtime, incidents.
