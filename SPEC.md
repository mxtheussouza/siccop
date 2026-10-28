# SPEC.md — Situational Awareness & Operational Coordination Platform

Product and domain specification. **What** to build. How/with-what is in `docs/DECISIONS.md`; rules of work are in `AGENTS.md`; evidence classes are in `docs/VERIFICATION.md`.

Requirement IDs (`AUTH-01`, …) are the unit of progress tracking. Class tags: `[A]` automated, `[E]` emulator/E2E, `[D]` physical device, `[M]` manual review.

## 1. Vision and non-goals

A modern command-and-control platform: operational awareness, interactive maps, agent/team tracking, incident management with atomic capture, operational actions, synchronization matrices, geospatial objects, reports, audit, realtime updates, and an offline-capable Android + iOS field app.

Inspired functionally by the Pacificador manual. **Do not copy** code, logos, trademarks, assets or visual identity. If `docs/reference/pacificador-manual.pdf` is absent, do not invent behavior beyond this spec.

Non-goals (v1): microservices, SSO login flow (backend must be OIDC-ready), mobile drawing of map objects, video, voice/PTT, third-party CAD integrations, tile server hosting (must be configurable for one).

Quality order: correctness → security/privacy → realtime responsiveness → offline resilience → performance → maintainability/observability.

## 2. Hierarchy and scoping

```
Organization → Command Center → Operation → { Memberships, Teams, Agents, Devices,
                                              Incidents, Map objects, Sync matrices, Reports }
```

All operational data is scoped by `operation_id`. Users must select an operation before accessing operational context. Cross-operation access is always 403.

Operation statuses: `PLANNED → ACTIVE ⇄ SUSPENDED → COMPLETED → ARCHIVED`. Mutations of operational data are allowed only in `ACTIVE` (reads allowed otherwise); `ARCHIVED` is read-only.

## 3. Roles and permission matrix

Roles: `ADMINISTRATOR` (organization-scoped, global role), and per-operation `CHIEF`, `OPERATOR`, `OBSERVER` via `OperationMembership`. A user may be CHIEF in one operation and OBSERVER in another. An ADMINISTRATOR has implicit CHIEF-level access to all operations of their organization; every such access to location history is audited.

| Capability                                                                                    | OBSERVER | OPERATOR | CHIEF |    ADMIN     |
| --------------------------------------------------------------------------------------------- | :------: | :------: | :---: | :----------: |
| View map, agents (live), incidents, POIs/routes/areas, sync matrices, reports                 |    ✔    |    ✔    |  ✔   |      ✔      |
| Create / edit incident, register action, capture, acknowledge, start, resolve                 |    –     |    ✔    |  ✔   |      ✔      |
| Assign team/agent to incident                                                                 |    –     |    ✔    |  ✔   |      ✔      |
| Close / cancel / reopen incident                                                              |    –     |    –     |  ✔   |      ✔      |
| Create/edit/delete POI, route, area                                                           |    –     |    ✔    |  ✔   |      ✔      |
| Import / delete geospatial layers                                                             |    –     |    –     |  ✔   |      ✔      |
| Manage teams, agent↔team, devices                                                            |    –     |    –     |  ✔   |      ✔      |
| Create/edit sync actions, change status                                                       |    –     |    ✔    |  ✔   |      ✔      |
| Create/delete matrix, clone matrix                                                            |    –     |    –     |  ✔   |      ✔      |
| Draft situation report                                                                        |    –     |    ✔    |  ✔   |      ✔      |
| Finalize situation report                                                                     |    –     |    –     |  ✔   |      ✔      |
| Location **history** / playback                                                               |    –     |    –     |  ✔   | ✔ (audited) |
| Manage users, organizations, command centers, operations, memberships, settings, audit viewer |    –     |    –     |   –   |      ✔      |
| Operation config (tracking policy, thresholds)                                                |    –     |    –     |  ✔   |      ✔      |

- `AUTHZ-01 [A]` Matrix enforced server-side by one policy layer; table-driven test covers every cell.
- `AUTHZ-02 [A]` Unauthenticated → 401; non-member → 403; insufficient role → 403.
- `AUTHZ-03 [A]` Operation isolation: no endpoint, query, WS channel or export returns another operation's data.

## 4. Entities (canonical names; English)

Identifiers are UUIDv7 unless stated. All timestamps `timestamptz`, UTC.

- **User**: id, email (unique, citext), display_name, password_hash (Argon2id), global_role (`ADMINISTRATOR`|`USER`), is_active, last_login_at, token_version.
- **Organization**, **CommandCenter** (organization_id), **Operation** (organization_id, command_center_id, name, code unique per organization, description, status, starts_at, ends_at, settings jsonb, created_by).
- **OperationMembership**: operation_id, user_id, role, unique(operation_id,user_id).
- **Team**: operation_id, name, call_sign (unique per operation), description, status.
- **Agent**: operation_id, team_id?, device_id?, call_sign (unique per operation), name, description, status (`AVAILABLE|ASSIGNED|MOVING|ON_SCENE|UNAVAILABLE|OFFLINE`), user_id? (agent may be linked to a user who logs into mobile), last_seen_at.
- **Device**: agent_id, platform (`ANDROID|IOS`), device_identifier_hash (hash of an app-generated install ID, never a hardware ID), app_version, last_seen_at, status (`PENDING|ACTIVE|REVOKED`), push_token?.
- **AgentLocation** (partitioned, append-only): agent_id, device_id, operation_id, geom Point(4326), accuracy_m, altitude_m, speed_mps, heading_deg, battery_pct, source (`GPS|NETWORK|MANUAL|IMPORT`), recorded_at (device, skew-corrected), recorded_at_raw, received_at, clock_adjusted bool. **AgentLatestLocation**: one row per agent, upserted only if newer.
- **IncidentType**: operation_id or organization default, name, default_priority, active.
- **Incident**: operation_id, reference_number (server-assigned, per operation sequence, human-readable), title, description, incident_type_id, priority (`LOW|MEDIUM|HIGH|CRITICAL`), status, location Point(4326), reported_by, claimed_by?, claimed_at?, assigned_team_id?, assigned_agent_id?, reported_at, acknowledged_at, started_at, resolved_at, closed_at, created_at, updated_at, **version int** (optimistic lock).
- **IncidentTransition** (append-only): incident_id, from_status, to_status, actor_id, occurred_at, reason.
- **IncidentAssignment** (append-only history): incident_id, team_id?, agent_id?, assigned_by, assigned_at, unassigned_at?.
- **IncidentAction** (append-only): incident_id, action_type, description, actor_id, occurred_at (client time, corrected), created_at (server). Corrections are new actions, never edits.
- **IncidentAttachment**: incident_id, action_id?, object_key, mime_type (sniffed), size_bytes, sha256, status (`PENDING_UPLOAD|SCANNING|READY|REJECTED`), thumbnail_key?, uploaded_by.
- **PointOfInterest**: operation_id, name, description, category, location Point, metadata jsonb, created_by, created_at, updated_at, version.
- **Route**: operation_id, name, description, geometry LineString, display_properties jsonb, metadata jsonb, version.
- **OperationalArea**: operation_id, name, description, geometry Polygon|MultiPolygon (valid, ST_IsValid), display_properties jsonb (color, opacity, visible), geofence_enabled, geofence_cooldown_s?, metadata jsonb, version.
- **MapLayer**: operation_id, name, source (`IMPORT`), geospatial_import_id, visible_default, style jsonb. **GeospatialImport**: operation_id, original_filename, detected_type (`KML|KMZ|GEOJSON`), size_bytes, sha256, status (`PENDING|PROCESSING|READY|FAILED`), feature_count, error?, created_by. Imported features stored as rows (`imported_feature`: layer_id, geom, properties jsonb) so they are queryable with PostGIS.
- **SynchronizationMatrix**: operation_id, name, description, starts_at, ends_at, created_by. **SynchronizationAction**: matrix_id, title, description, category, starts_at, ends_at, status (`PLANNED|DELAYED|IN_PROGRESS|COMPLETED|CANCELLED`), responsible_entity, created_by, version.
- **SituationReport**: operation_id, title, summary, content, author_id, reference_start, reference_end, status (`DRAFT|FINALIZED`), finalized_at, finalized_by, content_sha256 at finalization. Finalized reports are immutable; changes = new report referencing `supersedes_id`.
- **Notification**: user_id, operation_id?, type, title, body, data jsonb, read_at.
- **AuditEvent** (append-only, no UPDATE/DELETE grants): organization_id, operation_id?, actor_id?, action, entity_type, entity_id, occurred_at, metadata jsonb (no raw coordinates), correlation_id.
- **GeofenceState/GeofenceEvent**: agent_id, area_id, state (`INSIDE|OUTSIDE`), changed_at; event log of entered/exited.
- **IdempotencyRecord**: key, user_id, route, request_hash, response_status, response_body, created_at (TTL ≥ 7 days).
- **DomainEventOutbox**: id, operation_id, type, payload, created_at, published_at (see DECISIONS §Realtime).

## 5. State machines

**Incident** (server-validated, never client-set):

```
REPORTED → ACKNOWLEDGED → ASSIGNED → IN_PROGRESS → RESOLVED → CLOSED
   any non-terminal state → CANCELLED (CHIEF+)
   RESOLVED → IN_PROGRESS (reopen, CHIEF+, reason required)
```

Allowed forward skips: none, except `REPORTED → ASSIGNED` when assignment is made directly (implies acknowledge; two transitions recorded atomically). `CLOSED` and `CANCELLED` are terminal. Each transition requires `reason` where the table below says so and records an `IncidentTransition`.

| To                                            | Min role | Reason   |
| --------------------------------------------- | -------- | -------- |
| ACKNOWLEDGED, ASSIGNED, IN_PROGRESS, RESOLVED | OPERATOR | optional |
| CLOSED                                        | CHIEF    | optional |
| CANCELLED                                     | CHIEF    | required |
| reopen (RESOLVED→IN_PROGRESS)                 | CHIEF    | required |

**Capture (claim):** atomic, exactly-one-winner. Loser gets `409 INCIDENT_ALREADY_CLAIMED`. Release by claimer or CHIEF. Capture is independent of assignment.

**Sync action:** `PLANNED→IN_PROGRESS→COMPLETED`; `PLANNED|IN_PROGRESS→DELAYED→IN_PROGRESS`; any non-terminal→`CANCELLED`. `DELAYED` may also be derived-suggested when `ends_at` passes and status isn't COMPLETED (shown as a flag, never silently changed).

**Tracking state** (derived server-side, returned by API): `LIVE` (age ≤ stale_threshold), `STALE` (≤ offline_threshold), `OFFLINE` (older). Thresholds come from operation tracking policy; UI never hardcodes.

**Outbox (mobile):** `PENDING → PROCESSING → SYNCHRONIZED`; `PROCESSING → PENDING` (transient failure, backoff) ; `PROCESSING → FAILED` (needs user: conflict/validation).

## 6. Requirements

### Identity and administration

- `AUTH-01 [A]` Login/logout/refresh with rotating refresh tokens; reuse of an old refresh token revokes the whole token family.
- `AUTH-02 [A]` Argon2id hashing; password change revokes other sessions; account disable blocks login and refresh immediately.
- `AUTH-03 [A]` Short-lived access token; revocation via `token_version`.
- `AUTH-04 [A]` Rate limiting on login/refresh; generic error messages (no user enumeration).
- `AUTH-05 [E]` Web: no tokens in localStorage/sessionStorage. Mobile: tokens only in SecureStore. `[D]` for SecureStore behavior on devices.
- `AUTH-06 [M]` Backend structured so an OIDC provider can be added without changing authorization (identity linking table `user_identity`).
- `ADM-01..05 [A]` CRUD for users, organizations, command centers, operations, memberships; role changes audited.
- `OPS-01 [A]` Operation lifecycle with validated transitions; `OPS-02 [E]` operation selector gates all operational routes.

### Incidents

- `INC-01 [A]` Create (web list, web map context action, mobile) with idempotency key.
- `INC-02 [A]` Server-validated state machine; invalid transition → 409 `INVALID_TRANSITION`; every transition recorded.
- `INC-03 [A]` Atomic capture; N concurrent attempts → exactly one 2xx, N−1 409. Test with real PostgreSQL.
- `INC-04 [A]` Optimistic locking: `PATCH` requires `If-Match`/`version`; stale → 409 `VERSION_CONFLICT`.
- `INC-05 [A]` Append-only actions; no update/delete endpoints.
- `INC-06 [A]` Assignment to team/agent recorded in history; transactional with status change.
- `INC-07 [A]` Filters + cursor pagination (type, priority, status, assignment, bbox, text).
- `INC-08 [E]` List/detail/create/transition/capture/action UIs with five states.
- `ATT-01 [A]` Presigned upload/download; MIME sniffed from content (not extension), size cap, status lifecycle, thumbnails via worker, rejected files never downloadable.
- `ATT-02 [D]` Camera and photo library on both OSes with separate permissions; client-side compression.

### Geospatial

- `GEO-01 [A]` POI/route/area CRUD with validation (valid geometry, coordinate range, size caps) and optimistic locking.
- `GEO-02 [A]` Queries in PostGIS with GiST indexes: agents within radius, nearest N agents, incidents in bbox, objects inside area, tracks intersecting area. Plan check (`EXPLAIN`) asserts index use.
- `GEO-03 [A]` KML/GeoJSON import; KMZ import (see DECISIONS §Imports security); MIME/magic-byte validation; size/feature caps; deletion cascades to layer + features.
- `GEO-04 [E]` Web map: pan/zoom/fit bounds/fullscreen/current location/base layer switch/layer visibility/selection/context actions/filters.
- `GEO-05 [E]` Drawing and editing of POI, route, area on web.
- `GEO-06 [E]` Clustering for agents, incidents, POIs with click-to-expand; incremental source updates (no full re-render per agent move).
- `GEO-07 [M]` Base layers street/satellite/topographic/hybrid driven by configuration; missing provider config hides that layer rather than failing; no credentials in repo.

### Agents, devices, tracking

- `AGT-01 [A]` Agent/Team/Device CRUD and associations; device registration and revocation.
- `TRK-01 [A]` Batch ingest endpoint with per-point result (`accepted|duplicate|rejected(reason)`), idempotent by `(device_id, recorded_at)`; max batch and payload size enforced; rejects future timestamps beyond tolerance, bad coordinates, bad accuracy, non-member, device not associated.
- `TRK-02 [A]` Clock-skew correction per DECISIONS; flagged on the row.
- `TRK-03 [A]` Latest location upsert only if newer; Redis ephemeral state; PG is source of truth.
- `TRK-04 [A]` History query bounded (max window and max points, downsampling); returns GeoJSON LineString + points.
- `TRK-05 [A]` Retention job drops partitions older than policy; retention configurable.
- `TRK-06 [E]` Simulated device (script, clearly labeled dev tool) → API → WebSocket → marker moves on web. `[D]` for real Android and iOS GPS.
- `TRK-07 [D]` Android foreground vs background permission handling with rationale screens; foreground service notification; battery-aware policy.
- `TRK-08 [D]` iOS When-In-Use vs Always handling; background mode only when needed; lifecycle handling.
- `TRK-09 [A]` Tracking policy (min_interval, min_distance, desired_accuracy, batch_size, max_offline_buffer, stale/offline thresholds) stored per operation, served to clients.
- `TRK-10 [E]` History playback UI: play/pause/seek/speed/timeline over bounded data.
- `PRIV-01 [M]` Tracking indicator always visible on mobile while tracking; consent/explanation before OS permission prompt; privacy notice document; history access restricted (CHIEF+) and audited.

### Realtime

- `RT-01 [A]` Authenticated WS per operation; membership checked on connect and re-checked on role/membership change (server closes with 4403).
- `RT-02 [A]` Event envelope and catch-up per DECISIONS §Realtime; client reconnect with `last_event_id` replays missed events or receives `resync.required`.
- `RT-03 [A]` No global broadcast; event routing tests prove isolation between operations.
- `RT-04 [E]` Two browser clients: action in one appears in the other without refresh.

Event catalog (names fixed): `agent.location.updated`, `agent.status.updated`, `incident.created|updated|assigned|status.changed|claimed|released`, `incident.action.created`, `poi.created|updated|deleted`, `route.created|updated|deleted`, `area.created|updated|deleted`, `sync.action.created|updated|status_changed`, `notification.created`, `geofence.entered|exited`, `layer.created|deleted`, `resync.required`.

### Synchronization, reports, dashboard, audit

- `SYN-01 [A]` Matrix and action CRUD, clone (deep copy with new ids and shifted/unchanged dates option), filter, status changes via state machine.
- `SYN-02 [E]` Timeline view of actions with inspect panel.
- `REP-01 [A]` Reports from real queries: incident report, incident history, agent activity, operational timeline, situation report.
- `REP-02 [A]` CSV export; PDF export generated in worker for large reports.
- `REP-03 [A]` Situation report DRAFT→FINALIZED; finalized immutable; hash stored.
- `DASH-01 [E]` Dashboard from real aggregates only (active agents, online agents, open incidents, critical incidents, incidents by state, recent activity) + compact map + recent incidents + timeline. No synthetic data.
- `AUD-01 [A]` Append-only audit of login/logout, role changes, incident transitions, assignments, map object changes, report finalization, configuration changes; DB role cannot UPDATE/DELETE.
- `AUD-02 [E]` Admin audit viewer with filters and pagination.

### Notifications and geofencing

- `NOT-01 [A]` In-app notifications persisted and pushed over WS; read/unread.
- `NOT-02 [D]` Push via Expo Notifications on both OSes; permission requested with context, not at launch.
- `GEF-01 [A]` Entered/exited events computed with PostGIS on latest point; hysteresis + cooldown stored in Redis; one event per transition; storm prevention tested.

### Mobile application

- `MOB-01 [E]` Tabs: Mapa, Incidentes, Operação, Alertas, Perfil (Expo Router).
- `MOB-02 [E]` Map screen: own position, assigned/nearby incidents, team context, POIs, routes, areas, layers, filters, new-incident, center-on-me, tracking status.
- `MOB-03 [E]` Incident cards (priority, status, distance, assignment, timestamp) and detail (header, status, map, description, assignment, actions, attachments, timeline), bottom sheets.
- `MOB-04 [M]` Platform-appropriate UX on iOS and Android (safe areas, back behavior, edge-to-edge, keyboard); font scaling; tablet adaptive layout where practical.
- `MOB-05 [A]` Network/sync status always visible: Online / Offline / Synchronizing / Sync error. Never shows "synced" with pending items.
- `OFF-01 [A]` SQLite schema: `cached_operation`, `cached_incident`, `cached_assignment`, `cached_map_object`, `pending_command`, `pending_location`.
- `OFF-02 [A]` Outbox per DECISIONS §Offline: ordered, idempotent, retry with backoff, conflict surfaced.
- `OFF-03 [A]` Location buffer: write-ahead to SQLite before any network attempt; batch send; mark synced only on server ack; bounded buffer with documented eviction.
- `OFF-04 [E]` Offline → create incident/action → reconnect → exactly one server record. `[D]` on Android and iOS.

### Platform quality

- `OBS-01 [A]` Structured logs, correlation IDs, `/health` (liveness) and `/ready` (DB + Redis + storage), Prometheus metrics (request latency, error rate, active WS, location updates/s, incident events/s, DB pool, Redis status, worker failures), OpenTelemetry hooks.
- `SEC-01 [A]` Secure headers, CORS allowlist, rate limits, input validation, signed URLs, dependency scan in CI, secrets isolation.
- `SEC-02 [A]` No public tracking endpoint, WS or feed; coordinates not logged at INFO; location retention enforced.
- `PERF-01 [A]` No N+1 (query-count assertions on list endpoints), no unbounded queries, cursor pagination, virtualized tables on web.
- `PERF-02 [M]` Load-test scripts (Locust) for operators, WS clients, agents, concurrent ingestion, incident creation; results recorded with environment — no unmeasured claims.
- `DX-01 [A]` `make setup|infra-up|infra-down|migrate|seed|api|web|worker|mobile|test|lint|format|verify|contracts` work; CI runs verify for api/web/mobile without signing credentials.
- `DOC-01 [M]` Docs, ADRs 001–008, Mermaid diagrams (system, domain, realtime, tracking, offline sync, incident lifecycle).

## 7. API conventions

- Base `/api/v1`. Operation-scoped routes under `/operations/{operation_id}/…`.
- Mutating endpoints used by offline clients accept `Idempotency-Key`.
- Lists: cursor pagination `?cursor=&limit=` (default 50, max 200) with `next_cursor`.
- Times ISO-8601 UTC. IDs UUID. GeoJSON for geometry in API payloads.
- Representative endpoints are listed in the original brief and must exist: auth (login/refresh/logout), operations, agents, tracking batch, incidents (+transitions, actions, claim), pois, routes, areas, synchronization-matrices.

## 8. Development seed (dev only)

1 organization, 1 command center, 1 ACTIVE operation, users `admin@example.test`, `chief@example.test`, `operator@example.test`, `observer@example.test` (passwords documented in README, refused when `APP_ENV=production`), teams, agents, devices, incidents in several states, POIs, routes, areas (one geofenced), 1 sync matrix with actions.

## 9. Definition of done (product)

A developer can: clone → configure `.env` → `make infra-up migrate seed` → run api/web/mobile → log in → select operation → open map → create POI/route/area → create incident → see it in a second browser live → claim/assign/act → (simulated device) see agent move → run offline scenario on emulator → view history/playback → use matrix → generate reports → verify role limits → inspect audit. Items marked `[D]` are complete only when their checklists in `docs/mobile/` are ticked by a human on real Android and iOS devices.
