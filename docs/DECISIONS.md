# DECISIONS.md — Decisions already taken

These close the gaps left open in the original brief. Do not re-open them without an ADR that supersedes them. If a decision is infeasible in practice, apply the Blocker rule in `AGENTS.md §6` and record why.

## Versions

- Pin at Phase 01 after checking what is current; record the result in `docs/VERSIONS.md` and lock files (`uv.lock`, `pnpm-lock.yaml`). Never `latest` in manifests.
- Python 3.13. Node: current LTS. pnpm workspaces. Python deps managed with `uv`.
- Next.js: latest stable at bootstrap (App Router). React matching Next's requirement.
- Expo: latest stable SDK at bootstrap; install every Expo-related native package with `npx expo install` so versions stay SDK-compatible. Record the SDK number.
- PostgreSQL 17 + PostGIS 3.5 (container `postgis/postgis`), Redis 7+, MinIO.

## Backend stack choices

| Concern          | Choice                                                                                                                                                    |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Package/venv     | `uv`                                                                                                                                                      |
| Password hashing | `argon2-cffi` (Argon2id)                                                                                                                                  |
| Access token     | JWT via `PyJWT`, 10 min TTL, `kid` header for key rotation, claims: `sub`, `tv` (token_version), `typ=access`                                             |
| Refresh token    | Opaque random 256-bit, stored hashed (SHA-256) with `family_id`, `parent_id`, `used_at`, `revoked_at`, `expires_at` (default 14 days)                     |
| IDs              | UUIDv7 (client-generable)                                                                                                                                 |
| Migrations       | Alembic, one linear history, autogenerate then hand-review (GeoAlchemy2 index quirks)                                                                     |
| Worker           | **Dramatiq** with Redis broker (ADR-008). Rationale: simpler than Celery, good retries/middleware, sufficient for thumbnails, imports, PDF, retention.    |
| Object storage   | S3 API via `aioboto3` (or `boto3` in thread); MinIO locally; presigned URLs, 5 min TTL                                                                    |
| Rate limiting    | Redis token bucket in a dependency; per-IP for auth, per-user for others                                                                                  |
| Image processing | Pillow in worker (HEIC via `pillow-heif` → JPEG derivative)                                                                                               |
| MIME sniffing    | `python-magic` (libmagic) on bytes; extension and client Content-Type are untrusted                                                                       |
| XML              | `defusedxml` only. Plain `xml`/`lxml` default parsers are forbidden for untrusted input                                                                   |
| Geometry         | PostGIS for computation; Shapely only for small validation/serialization tasks                                                                            |
| Metrics          | `prometheus-client`; OTel via `opentelemetry-instrumentation-fastapi/sqlalchemy/redis`                                                                    |
| Load tests       | Locust                                                                                                                                                    |
| Typing           | Pyright strict on `src/`; third-party gaps handled with stubs in `apps/api/typings/` or narrow, commented `# pyright: ignore[rule]` (GeoAlchemy2/Shapely) |

## Errors

All non-2xx API responses:

```json
{
  "type": "conflict",
  "title": "Incident already claimed",
  "status": 409,
  "detail": "Human readable, no internals",
  "code": "INCIDENT_ALREADY_CLAIMED",
  "correlation_id": "…",
  "errors": [{ "field": "…", "message": "…" }] // validation only
}
```

`type` ∈ `validation|unauthorized|forbidden|not_found|conflict|rate_limited|not_implemented|internal`. Codes are UPPER_SNAKE and part of the OpenAPI contract. `X-Correlation-ID` is accepted and echoed.

## Authentication topology

- **Same-origin for web.** Production: nginx serves Next.js and proxies `/api/*` and `/ws/*` to FastAPI. Dev: Next.js `rewrites` proxy `/api/*` to the API. Cookies are therefore first-party.
- **Web:** access token held **in memory only**; refresh token in an `HttpOnly; Secure; SameSite=Strict; Path=/api/v1/auth` cookie set by the API. Page load calls `/auth/refresh` to bootstrap. CSRF: SameSite=Strict + strict `Origin`/`Host` check on cookie-authenticated endpoints (`/auth/refresh`, `/auth/logout`). API calls use `Authorization: Bearer`.
- **Mobile:** header `X-Client: mobile` → refresh token returned in the body and stored in SecureStore; no cookies.
- **Refresh rotation:** each use issues a new refresh token, marks parent used; reuse of a used token revokes the family and returns 401 `REFRESH_REUSE_DETECTED`.
- Password change/disable increments `token_version` and revokes families.

## Realtime

- **Event envelope** (all WS messages and all stored events):

```json
{
  "event_id": "<redis stream id>",
  "type": "incident.status.changed",
  "operation_id": "…",
  "sequence": 1234,
  "occurred_at": "…",
  "entity_id": "…",
  "entity_version": 7,
  "schema_version": 1,
  "correlation_id": "…",
  "payload": {}
}
```

Payloads are **minimal deltas or ids + version**, never large objects; clients refetch details via REST when `entity_version` is ahead of their cache.

- **Transactional outbox:** domain events are inserted into `domain_event_outbox` in the **same DB transaction** as the change. A relay (in the worker, polling with `FOR UPDATE SKIP LOCKED`, interval ≤ 200 ms, or LISTEN/NOTIFY wake-up) publishes to Redis and sets `published_at`. Delivery is at-least-once; consumers dedupe by `event_id`.
- **Redis Streams** per operation: `ops:{operation_id}:events`, `MAXLEN ~ 10000`. `sequence` is an `INCR` counter `ops:{operation_id}:seq` assigned at publish time. (Pub/Sub is not used for durable events.)
- **Ephemeral high-rate events** (`agent.location.updated`): published directly after commit to a separate capped stream/channel, **not replayed**; latest state lives in Redis hash `ops:{id}:agents:latest` and in PG `agent_latest_location`. Reconnecting clients take a snapshot.
- **Connect:** client calls `POST /api/v1/realtime/tickets {operation_id}` (authenticated) → single-use ticket (TTL 30 s, bound to user+operation+IP-hash) → opens `/ws/operations/{operation_id}?ticket=…&last_event_id=…`. Ticket in URL is harmless because single-use and short-lived. Tokens never go in the URL.
- **Catch-up:** if `last_event_id` is within the stream window, replay then go live; otherwise send `resync.required` and the client refetches via REST.
- **Authorization lifecycle:** membership/role/user-disable changes publish an internal event; the gateway re-checks and closes with code 4403. Heartbeat ping 20 s; server drops after 2 missed pongs.
- **Backpressure:** per-connection bounded queue; slow consumers are closed (code 4408) and must resync. Max message 16 KB.
- Gateway runs in the API process initially; multiple API instances work because they all consume Redis.

## Tracking

- `agent_locations` is **declaratively partitioned by month on `recorded_at`**. Indexes per partition: btree `(agent_id, recorded_at DESC)`, unique `(device_id, recorded_at)`, GiST on `geom` (created for recent partitions; older partitions may drop GiST). Partitions created ahead by a maintenance job; retention drops whole partitions.
- **Dedupe:** `INSERT … ON CONFLICT (device_id, recorded_at) DO NOTHING`; response reports per point `accepted|duplicate|rejected`. Client assigns `client_point_id` (UUID) echoed back.
- **Batch limits:** ≤ 500 points, ≤ 256 KB. Reject `recorded_at > received_at + 60 s`. Accept old points up to retention. Accuracy > `max_accuracy_m` (policy, default 200) is stored with flag `low_accuracy` but excluded from latest-location updates.
- **Clock skew:** client sends `device_sent_at`. `skew = received_at − device_sent_at`; if `|skew| > 30 s`, store `recorded_at = recorded_at_raw + skew`, set `clock_adjusted = true`.
- **Default tracking policy** (per operation, editable by CHIEF): `minimum_interval_s=10` (moving) / `60` (idle), `minimum_distance_m=15`, `desired_accuracy=balanced` (`high` when agent is ASSIGNED/ON_SCENE), `batch_size=50`, `maximum_offline_buffer=5000`, `stale_threshold_s=120`, `offline_threshold_s=600`, `retention_days=30`, `max_accuracy_m=200`, `geofence_cooldown_s=60`.
- Tracking state (LIVE/STALE/OFFLINE) is computed by the API from the latest **corrected recorded_at**, using the policy thresholds, and returned with the agent payload.
- **History:** max window 24 h per request, max 5,000 points per response (server-side downsampling with `ST_SimplifyPreserveTopology`/time bucketing), cursorable.
- **Geofencing:** evaluated after commit on the _latest accepted point per agent per batch_ (not every buffered point) using `ST_Covers` against `geofence_enabled` areas (GiST). State per (agent, area) in Redis + PG; emit only on state change and only if outside `geofence_cooldown_s` since last event for that pair. Offline-replayed points older than 5 min do not emit geofence events (they are history only).

## Offline (mobile)

**Commands that may be created offline** (everything else requires connectivity and the UI says so):

| command_type                  | Notes                                                                              |
| ----------------------------- | ---------------------------------------------------------------------------------- |
| `incident.create`             | Client UUID; server assigns `reference_number`, reconciled on sync                 |
| `incident.action.create`      | Append-only; client UUID; `occurred_at` from device clock (skew-corrected on sync) |
| `incident.attachment.upload`  | Depends on parent create; uploaded after parent is synchronized                    |
| `incident.transition.request` | Only `ACKNOWLEDGED`, `IN_PROGRESS`, `RESOLVED`; sends `expected_from_status`       |
| `tracking.locations.batch`    | Handled by the location buffer (separate table), not the command outbox            |

Not offline: capture/claim, assignment, close/cancel, map-object edits, reports, admin.

**Outbox rules:** strict FIFO **per operation**; a command with `depends_on` waits for it. Each request carries `Idempotency-Key = outbox.idempotency_key`. Server stores idempotency records ≥ 7 days; replays return the original response. Transient errors (network, 5xx, 429) → back to `PENDING` with exponential backoff + jitter, `attempt_count++`. Validation/authorization/conflict (4xx except 408/429) → `FAILED` with `error_code`; nothing auto-overwrites server state. User can **retry**, **edit**, or **discard**; discarding a command that others depend on discards dependents after confirmation.
**Conflict policy:** server truth wins. `STATE_CONFLICT` (transition no longer valid) and `VERSION_CONFLICT` are surfaced to the user with current server state; no silent last-write-wins.
**Sync UI states:** Online, Offline, Synchronizing (n pending), Sync error (n failed). Badge counts come from SQLite, not memory.
**Location buffer:** every fix is written to `pending_location` **before** any network attempt; sent in batches of `batch_size`; rows deleted/marked only after server ack per point; eviction when full: drop oldest points that are within `minimum_distance` of neighbours first, then oldest overall; eviction count is shown in tracking status.

## Web map

- MapLibre GL JS; drawing via **Terra Draw** (`terra-draw` + MapLibre adapter).
- Realtime agent movement updates a GeoJSON source with `setData` on a throttled (≤ 4 Hz) diff, never re-creating layers.
- Clustering via MapLibre source `cluster: true`.
- Base layers from config `MAP_BASE_LAYERS` (JSON: id, label, style URL or raster tiles template, attribution, optional key via env). Dev default: MapLibre demo tiles style (low detail, **dev only**). Public OSM tile servers must not be used as a production default (usage policy). Production guidance in docs: self-hosted PMTiles/vector tiles or a commercial provider.
- Satellite/topographic/hybrid appear only if configured.

## Mobile map

- `@maplibre/maplibre-react-native` (requires a development build; not Expo Go). Same style config as web.
- v1 mobile **views** POIs/routes/areas/layers and places incidents by tap/long-press; drawing is web-only.
- If MapLibre RN proves incompatible with the pinned Expo SDK, fall back to the SDK-compatible choice, record an ADR, and note in LIMITATIONS.

## Imports security (KML / KMZ / GeoJSON)

- Upload to object storage first (presigned), then validate/parse **in the worker**.
- Size caps: upload ≤ 10 MB; KMZ uncompressed total ≤ 50 MB; entries ≤ 100; compression ratio ≤ 100:1; reject absolute paths and `..`; read only the root `doc.kml` (or first `*.kml`), ignore other entries (no extraction to disk).
- Sniff bytes: GeoJSON (JSON object with `type`), KML (XML root `kml`), KMZ (ZIP magic + contains kml). Extension ignored.
- XML via `defusedxml`; any DOCTYPE/entity declaration → reject.
- Feature cap 10,000 per import; coordinates validated to WGS84 range; geometries made valid (`ST_MakeValid`) or rejected; Z/M dropped. Network links (`NetworkLink`, remote icons) are **ignored and never fetched**.
- Result: `GeospatialImport` + `MapLayer` + `imported_feature` rows. Deleting the import deletes all of them.

## Attachments

- Flow: `POST …/attachments` (declares name, claimed type, size) → presigned PUT → client `POST …/attachments/{id}/complete` → worker sniffs, hashes, thumbnails → `READY` or `REJECTED`. Download only when `READY`, via presigned GET (5 min).
- Allowed: `image/jpeg`, `image/png`, `image/webp`, `image/heic`(converted), `application/pdf`. Max 15 MB (photos compressed client-side to long edge ≤ 2048 px, quality ~0.8).
- Bucket private; keys `operations/{operation_id}/incidents/{incident_id}/{uuid}`.

## Privacy / LGPD (location data)

- A written privacy notice and legal-basis statement is a **human deliverable** (`docs/security/privacy.md` created as a template; the controller completes it). The agent must not assert a legal basis.
- Data minimization: device identifier is an app-generated random install ID, hashed; no IMEI/advertising ID.
- Transparency: persistent tracking indicator in the mobile app; explanation screen before each OS location prompt; tracking only while the agent is on an ACTIVE operation and has enabled it (unless operation policy marks tracking mandatory — displayed to the agent).
- Access: live positions visible to all operation members; **history/playback CHIEF+ only**, each access audited (who, which agent, window — not coordinates).
- Retention: per-operation `retention_days` enforced by partition drop job; documented export and deletion procedure for a data subject request.
- Logs and audit metadata never contain raw coordinates.

## Security baseline

Secure headers (CSP with nonce for Next.js, HSTS in prod, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy` allowing geolocation only for self), CORS allowlist from config, request body size limits, pagination caps, SSRF-safe (no server-side fetch of user URLs), dependency scanning in CI (`pip-audit`/`uv`, `pnpm audit`, optional Trivy for images), secret scanning (gitleaks) in CI.

## Testing policy

- Backend: pytest + pytest-asyncio + Testcontainers (PostGIS, Redis, MinIO). If Docker is unavailable the container tests are reported **NOT RUN**.
- Web: Vitest + Testing Library; Playwright for critical flows (against dev stack).
- Mobile: Jest (shared logic, outbox, location buffer, validation) using `expo-sqlite` against an in-memory/real SQLite in Node (`better-sqlite3` adapter in tests); Maestro flows for emulator E2E where an emulator exists.
- Concurrency tests use real PostgreSQL with parallel clients (≥ 20 concurrent claims).

## ADR list (create in Phase 01 from this file, expanded with trade-offs)

001 modular monolith · 002 FastAPI · 003 PostgreSQL+PostGIS (incl. partitioning) · 004 Redis (Streams vs Pub/Sub, ephemeral state) · 005 WebSocket (tickets, envelope, catch-up) · 006 mobile offline outbox · 007 object storage · 008 background worker (Dramatiq) · 009 auth topology (same-origin, refresh cookie, rotation) · 010 transactional event outbox · 011 map libraries (MapLibre, Terra Draw, MapLibre RN).
