# Phase 13 — Hardening: observability, performance, security, privacy

**Objective:** make the system operable, measurable and defensible. Measure first; optimize only what measurements justify.

**Read:** SPEC §6 (OBS-01, SEC-01/02, PERF-01/02, PRIV-01), DECISIONS (Security baseline, Privacy/LGPD, Testing policy).

## Tasks

1. Observability: Prometheus metrics (request latency histograms, error rate, active WebSockets, location points/s, incident events/s, DB pool usage, Redis status, outbox lag, worker failures/queue depth); OpenTelemetry tracing wired for FastAPI/SQLAlchemy/Redis/Dramatiq with correlation propagation; Grafana dashboards provisioned from files in `infrastructure/monitoring`; alert rules examples (outbox lag, 5xx rate, WS drops).
2. Security review checklist executed and recorded in `docs/security/security-model.md`: threat model (assets: location data, incident data, credentials), authn/authz, tenant isolation, WS ticket model, file handling, imports, rate limits, headers/CORS/CSP, secrets, dependency/image scanning, logging hygiene. Add automated tests for: security headers present, CORS allowlist, rate limits, oversized bodies, ID enumeration returns 404/403 consistently, WS without ticket rejected, no public endpoints beyond health/login/refresh.
3. Authorization sweep: script that enumerates every route from OpenAPI and asserts each has a declared permission or is on an explicit public allowlist (test fails if a new route lacks it).
4. Privacy: complete `docs/security/privacy.md` as a **template for the controller** (data inventory, purposes, retention, access, subject-request procedure for export/deletion implemented as admin CLI/endpoint), no legal-basis assertion; verify log hygiene tests (no coordinates, tokens, presigned URLs at INFO+); retention job covered by tests.
5. Performance: query review with `EXPLAIN (ANALYZE, BUFFERS)` for hot paths (incident list, bbox, ingest, latest agents, dashboard); add/adjust indexes only with before/after evidence; connection-pool sizing documented; ingest batching verified.
6. Load tests (Locust) in `tools/loadtest`: operators browsing/creating incidents, many WebSocket clients, many simulated agents posting batches, concurrent claims. README with how to run, environment recording template, and results file format. **Run what the environment allows**, record environment + numbers; state clearly if a full run was not possible. Never claim capacity beyond what was measured.
7. Resilience checks: Redis down (API degrades, `/ready` reports, outbox keeps queueing), worker down (jobs queue, UI shows pending), DB failover reconnect, WS reconnect storm.
8. CI additions: scheduled dependency audit, container scan, SBOM artifact; coverage thresholds enforced.

## Tests

- Metrics endpoint exposes the named series after exercised traffic.
- Security tests listed in task 2/3 (AUTO).
- Resilience tests with Testcontainers stopping Redis mid-test.
- Load smoke (short, small) runs in CI-compatible mode; full runs are manual and documented.

## Exit criteria

- `make verify` green; OBS-01, SEC-01, SEC-02, PERF-01 evidence; PERF-02 scripts present with at least one recorded run (with environment) or a LIMITATIONS entry explaining why not.
- `docs/security/security-model.md` and `docs/security/privacy.md` complete (privacy legal fields clearly marked "controller to complete").

## Out of scope

Premature optimization without measurements; changing architecture to microservices.
