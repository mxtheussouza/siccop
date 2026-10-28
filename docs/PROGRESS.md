# PROGRESS.md

The agent's memory between sessions. **Read first, update last.** Keep it short and factual. Never mark a requirement `DONE` without the evidence its class requires (`docs/VERIFICATION.md`).

## Current state

- Current phase: 01 complete (2026-10-28). Next: Phase 02.
- Last session: 2026-10-28 (third resume, new Linux/WSL2 host with network and Docker)
- Last `make verify`: exit 0 (2026-10-28), with `.next/dev` artifacts present from a prior `make web`
- Milestone reached: none (M1 is after Phase 05)

## Environment (refreshed 2026-10-28)

| Probe                  | Result                                                                                                             |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------ |
| OS                     | Ubuntu 26.04 LTS on WSL2, x86_64 (kernel 6.6.87.2-microsoft-standard-WSL2)                                         |
| Docker available       | Yes: Engine 29.5.1, Compose 5.1.3; `docker info` succeeds                                                          |
| Android SDK / emulator | `adb` and `emulator` not found                                                                                     |
| Xcode / iOS simulator  | Not possible on Linux                                                                                              |
| Node / pnpm            | Node 24.18.0 (official tarball in `~/.local/share`, SHA-256 verified; system Node is 22); pnpm 12.4.2 via Corepack |
| Python / uv            | uv 0.13.4 (`~/.local/bin`); uv-managed CPython 3.13.16 for the API; system Python 3.14.4 unused                    |
| Pinned versions file   | docs/VERSIONS.md (installed versions)                                                                              |
| Registry access        | npm, PyPI, Docker Hub reachable. `minio/minio` and `minio/mc` no longer exist on Docker Hub (L-123)                |
| Git                    | Repository present on `main`                                                                                       |

## Phases

| Phase | Title                                                    | Status      | Date       | Notes                                                                                                                              |
| ----- | -------------------------------------------------------- | ----------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 01    | Bootstrap                                                | DONE        | 2026-10-28 | All exit criteria passed on Linux/WSL2 (see Phase 01 completion evidence). Native builds and CI runs not performed (L-114, L-125). |
| 02    | Identity, hierarchy, operations, RBAC, audit foundation  | NOT-STARTED |            |                                                                                                                                    |
| 03    | Web shell, design system, auth UI                        | NOT-STARTED |            |                                                                                                                                    |
| 04    | Incidents backend                                        | NOT-STARTED |            |                                                                                                                                    |
| 05    | Realtime + incidents web UI (M1)                         | NOT-STARTED |            |                                                                                                                                    |
| 06    | Object storage, worker, attachments                      | NOT-STARTED |            |                                                                                                                                    |
| 07    | Geospatial backend + web map                             | NOT-STARTED |            |                                                                                                                                    |
| 08    | Agents, teams, devices, tracking, realtime map (M2)      | NOT-STARTED |            |                                                                                                                                    |
| 09    | Mobile shell, auth, map, tracking, online incidents (M3) | NOT-STARTED |            |                                                                                                                                    |
| 10    | Offline: SQLite, outbox, location buffer (M4)            | NOT-STARTED |            |                                                                                                                                    |
| 11    | Sync matrices, reports, dashboard                        | NOT-STARTED |            |                                                                                                                                    |
| 12    | Notifications, geofencing, history playback              | NOT-STARTED |            |                                                                                                                                    |
| 13    | Hardening: observability, load, security, privacy        | NOT-STARTED |            |                                                                                                                                    |
| 14    | Documentation, final validation (M5)                     | NOT-STARTED |            |                                                                                                                                    |

## Requirement status

One row per expanded SPEC requirement. Multiple classes retain every evidence obligation. No requirement is DONE.

```text
AUTHZ-01 | AUTO | NOT-STARTED |
AUTHZ-02 | AUTO | NOT-STARTED |
AUTHZ-03 | AUTO | NOT-STARTED |
AUTH-01 | AUTO | NOT-STARTED |
AUTH-02 | AUTO | NOT-STARTED |
AUTH-03 | AUTO | NOT-STARTED |
AUTH-04 | AUTO | NOT-STARTED |
AUTH-05 | EMU+DEVICE | NOT-STARTED |
AUTH-06 | MANUAL | NOT-STARTED |
ADM-01 | AUTO | NOT-STARTED |
ADM-02 | AUTO | NOT-STARTED |
ADM-03 | AUTO | NOT-STARTED |
ADM-04 | AUTO | NOT-STARTED |
ADM-05 | AUTO | NOT-STARTED |
OPS-01 | AUTO | NOT-STARTED |
OPS-02 | EMU | NOT-STARTED |
INC-01 | AUTO | NOT-STARTED |
INC-02 | AUTO | NOT-STARTED |
INC-03 | AUTO | NOT-STARTED |
INC-04 | AUTO | NOT-STARTED |
INC-05 | AUTO | NOT-STARTED |
INC-06 | AUTO | NOT-STARTED |
INC-07 | AUTO | NOT-STARTED |
INC-08 | EMU | NOT-STARTED |
ATT-01 | AUTO | NOT-STARTED |
ATT-02 | DEVICE | NOT-STARTED |
GEO-01 | AUTO | NOT-STARTED |
GEO-02 | AUTO | NOT-STARTED |
GEO-03 | AUTO | NOT-STARTED |
GEO-04 | EMU | NOT-STARTED |
GEO-05 | EMU | NOT-STARTED |
GEO-06 | EMU | NOT-STARTED |
GEO-07 | MANUAL | NOT-STARTED |
AGT-01 | AUTO | NOT-STARTED |
TRK-01 | AUTO | NOT-STARTED |
TRK-02 | AUTO | NOT-STARTED |
TRK-03 | AUTO | NOT-STARTED |
TRK-04 | AUTO | NOT-STARTED |
TRK-05 | AUTO | NOT-STARTED |
TRK-06 | EMU+DEVICE | NOT-STARTED |
TRK-07 | DEVICE | NOT-STARTED |
TRK-08 | DEVICE | NOT-STARTED |
TRK-09 | AUTO | NOT-STARTED |
TRK-10 | EMU | NOT-STARTED |
PRIV-01 | MANUAL | NOT-STARTED |
RT-01 | AUTO | NOT-STARTED |
RT-02 | AUTO | NOT-STARTED |
RT-03 | AUTO | NOT-STARTED |
RT-04 | EMU | NOT-STARTED |
SYN-01 | AUTO | NOT-STARTED |
SYN-02 | EMU | NOT-STARTED |
REP-01 | AUTO | NOT-STARTED |
REP-02 | AUTO | NOT-STARTED |
REP-03 | AUTO | NOT-STARTED |
DASH-01 | EMU | NOT-STARTED |
AUD-01 | AUTO | NOT-STARTED |
AUD-02 | EMU | NOT-STARTED |
NOT-01 | AUTO | NOT-STARTED |
NOT-02 | DEVICE | NOT-STARTED |
GEF-01 | AUTO | NOT-STARTED |
MOB-01 | EMU | NOT-STARTED |
MOB-02 | EMU | NOT-STARTED |
MOB-03 | EMU | NOT-STARTED |
MOB-04 | MANUAL | NOT-STARTED |
MOB-05 | AUTO | NOT-STARTED |
OFF-01 | AUTO | NOT-STARTED |
OFF-02 | AUTO | NOT-STARTED |
OFF-03 | AUTO | NOT-STARTED |
OFF-04 | EMU+DEVICE | NOT-STARTED |
OBS-01 | AUTO | IN-PROGRESS | Logs/correlation ID, /health, /ready done and tested (tests/unit/test_http.py, tests/integration/test_infrastructure.py::test_postgis_migration_and_readiness_redis_outage). Prometheus metrics and OTel are Phase 13 (L-117).
SEC-01 | AUTO | NOT-STARTED |
SEC-02 | AUTO | NOT-STARTED |
PERF-01 | AUTO | NOT-STARTED |
PERF-02 | MANUAL | NOT-STARTED |
DX-01 | AUTO | IMPLEMENTED-UNVERIFIED | All make targets ran locally (seed is an intentional NOT_IMPLEMENTED until Phase 02, L-115). CI workflows not yet run (L-125); security.yml audit expected to fail (L-124).
DOC-01 | MANUAL | NOT-STARTED |
```

Phase 01 initial-session evidence (2026-10-21, before resume):

- `python3 tools/check_phase.py`: 76 requirement IDs/classes, ADR-001..011 and exact JS direct pins checked; passed.
- `python3 -m unittest discover -s tools/tests -v`: 2 inventory-tool tests passed on host Python 3.14.7.
- `node --test packages/config/tests/*.test.mjs`: 1 shared strict-configuration test passed on Node 24.18.0.
- Python AST / JSON / TOML / JavaScript syntax checks passed; `docker compose --env-file .env.example config --quiet` passed configuration validation only.
- `make verify`: exit 2 at format-check (Python download DNS failure); no downstream gate stage ran.
- `make phase-check`: source inventory passed, then exit 2 at contracts-check (Corepack/npm DNS failure); Expo config did not run.
- `make test-integration`: exit 2 with explicit NOT RUN (Docker daemon unavailable).
- `make lock`: exit 2 (required Python download DNS failure); no locks generated.

These results do not verify API/web/mobile behavior. No requirement is DONE and Phase 01 must be resumed before Phase 02.

## Resume evidence (2026-10-21)

- Removed the Makefile default `UV_PYTHON_INSTALL_DIR` override; it hid the already installed host runtime. `uv python find --no-python-downloads 3.13.16` and `apps/api/.venv/bin/python --version` confirm CPython 3.13.16.
- `make lock`: Python selected successfully, then failed resolving PyPI (`https://pypi.org/simple/fastapi/`, DNS). Independent `pnpm install --lockfile-only`, `make contracts` and `make phase-check` fail acquiring pinned pnpm 12.4.2 from npm (ENOTFOUND). No lock/schema artifacts generated.
- `docker desktop start`: attempted; reported denied writes to Docker's host log directory and did not confirm startup. Desktop UI access timed out; application launch by name was unavailable. `make infra-up` failed with permission denied on the Docker socket. No container health or migration result is claimed.
- `make test-integration`: explicit NOT RUN; session cannot access Docker. `make verify`: exit 2 at format-check because the authoritative Python lock is absent; no checks were skipped to produce a green gate.
- `apps/api/.venv/bin/python -m unittest discover -s tools/tests -v`: 2 tests passed under Python 3.13.16. `node --test packages/config/tests/*.test.mjs`: 1 test passed. These are tooling/configuration tests, not app behavior.
- Source inventory passes with 76 current requirement IDs (including AUTHZ-01..03) and 11 ADRs. Compose config validation passes; runtime health remains unverified.
- Local `.env` was created from development-only examples with mode 0600; it is ignored and an existing file is preserved.

## Second-resume evidence (2026-10-21)

- Both lock files and pinned pnpm 12.4.2 were present when this resume inspected the workspace. Preserved them; did not reconstruct package metadata by hand.
- `make lock setup`: make lock PASSED (uv resolved 86 packages; pnpm validated all 7 workspace projects), then setup FAILED downloading locked Python packages from files.pythonhosted.org (DNS). `uv lock --check --offline --project apps/api` also passed.
- Independent frozen JavaScript installation with a workspace-local store was attempted; npm tarball downloads fail DNS. No package pins or validation rules were weakened. Pinned Ruff is not available in the offline cache.
- `make verify`: FAILED at format-check while uv tried to install locked dependencies; Ruff did not execute. `make contracts` / `make phase-check` cannot run their generator until JavaScript/API dependencies are installed.
- `docker desktop start --detach --timeout 15`: returned 0 with Starting Docker Desktop after host-log permission warnings. Subsequent `docker info` and `make infra-up` fail because the socket is absent; container startup is not verified. Integration suite reports explicit NOT RUN.
- Local source inventory, 2 Python tooling tests, 1 Node configuration test and Compose config validation passed again. No API/web/mobile runtime or native build evidence was produced.

## Phase 01 completion evidence (2026-10-28)

- `make setup`: passed (uv sync from `uv.lock`; `pnpm install --frozen-lockfile`; `expo install --check` → dependencies up to date).
- `make verify`: exit 0. Stages: ruff format/lint, prettier, eslint, pyright strict (0 errors), tsc for 6 workspaces, pytest unit 20 passed (API coverage 76%), vitest 1, jest 1, node:test 1, tooling unittest 2, integration 1 passed (real PostGIS/Redis/MinIO via Testcontainers), API sdist/wheel, `next build`, `expo export` Android+iOS, contracts-check.
- `make phase-check`: exit 0 (inventory, contracts freshness, Expo public config).
- `make infra-up`: database, redis, storage, storage-bootstrap healthy; with `--profile worker --profile monitoring`, worker, prometheus and grafana also healthy. `make migrate`: revision 0001 applied; PostgreSQL 17.5, PostGIS 3.5.2.
- `make api` + curl: `/health` 200; `/ready` 200; `docker compose stop redis` → `/ready` 503 `DEPENDENCY_UNAVAILABLE`; after restart → 200.
- `make web` + curl: `/login` 200 with the disabled "Entrar indisponível" action.
- `pnpm --filter @platform/mobile prebuild-check`: passed (generated native dirs removed; gitignored). Warning: `userInterfaceStyle` on Android needs `expo-system-ui` (backlog).
- `make contracts`: `openapi.json` and `schema.d.ts` generated and committed; `contracts-check` leaves no diff.
- gitleaks v8.24.2: no leaks. `pip-audit`: no known vulnerabilities. `pnpm audit`: 3 remaining (L-124).
- Not run: GitHub Actions (L-125), native Android/iOS builds, emulators, devices (L-114, L-103).

Fixes made while getting to green: Ruff/Prettier formatting applied; Ruff per-file-ignore glob fixed so test asserts match; pyright strict errors fixed (typed `ApplicationError` attributes, explicit handler/route registration, `load_settings()`, typed S3 client); **the storage readiness probe used `with boto3 client`, which is not a context manager, so `/ready` would always report storage down; replaced with try/finally close**; `check_phase.py` excluded `.venv`/`dist`; integration test stops Redis without removing the container.

## Decisions beyond DECISIONS.md

(date · phase · decision · reason — also create an ADR if architectural)

- 2026-10-28 · 01 · Local MinIO from the archived `bitnamilegacy/minio:2025.4.22` (digest-pinned) · Official images are gone; same MinIO/mc commits as the original pins; dev/test only (L-123).
- 2026-10-28 · 01 · Temporary exact-version `minimumReleaseAgeExclude` for Expo SDK 58 patches · `expo install --check` requires them; expires 2026-10-28T16:15Z (L-121).
- 2026-10-28 · 01 · pnpm install scripts denied for esbuild, @parcel/watcher, unrs-resolver · Each ships prebuilt optional binaries; least privilege; all tests and builds pass.
- 2026-10-28 · 01 · TypeScript 6.0.3 (root); contracts keeps 5.9.3 · Next 16.4.2 typings require TS 6 `URLPattern`; openapi-typescript peers on TS 5.
- 2026-10-28 · 01 · Mobile `skipLibCheck: true` · Third-party Expo/RN declarations fail full lib checking; app code still strict (L-122).
- 2026-10-28 · 01 · Web tsconfig no longer includes `.next/dev/types` · Duplicate global declarations with `.next/types` broke `next build`/typecheck after any `next dev` run; `next dev` does not re-add it.

## Backlog (noticed, belongs to another phase)

- Phase 09: `app.config.ts` sets `userInterfaceStyle`; Android needs `expo-system-ui` for it (prebuild warning).
- Phase 13: starlette TestClient warns that `httpx` is deprecated in favor of `httpx2`.

- CORRECTED (2026-10-21, resume): AUTHZ-01..03 are present in SPEC.md and both inventories. The previous backlog claim that they were missing was incorrect; no requirement or Phase 02 implementation was added.
- Seed is an explicit NOT_IMPLEMENTED command until the Phase 02 domain model exists.
- API/worker metrics and OpenTelemetry remain Phase 13; bootstrap monitoring has no synthetic domain data.

## Blocked

- Nothing blocks Phase 02. Open items: L-114 (native toolchains), L-121 (remove release-age exclusions after 2026-10-28T16:15Z), L-123 (MinIO image choice before Phase 06), L-124 (audit advisories), L-125 (run CI).

## Human sign-offs

| Item | Who | Date | Device / env | Result |
| ---- | --- | ---- | ------------ | ------ |
