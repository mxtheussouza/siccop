# PROGRESS.md

The agent's memory between sessions. **Read first, update last.** Keep it short and factual. Never mark a requirement `DONE` without the evidence its class requires (`docs/VERIFICATION.md`).

## Current state

- Current phase: 01 (bootstrap in progress; not complete)
- Last session: 2026-10-21 (second resume: real locks validated; installation/Docker still blocked)
- Last `make verify`: FAILED at format-check (exit 2); the Python lock is present, but locked package downloads fail DNS. Ruff and all downstream gate stages did not run.
- Milestone reached: none

## Environment (fill in Phase 01, refresh when it changes)

| Probe                  | Result                                                                                                                                                                                         |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Docker available       | CLI 29.8.0 / Compose 5.5.1. Detached Desktop start returned 0 with Starting Docker Desktop; docker info / infra-up still fail because the socket is absent. Server availability is unverified. |
| OS                     | macOS / Darwin 27.0.0, arm64                                                                                                                                                                   |
| Android SDK / emulator | `adb` and `emulator` not found                                                                                                                                                                 |
| Xcode / iOS simulator  | Command Line Tools only; `xcodebuild` and `simctl` unavailable                                                                                                                                 |
| Node / pnpm            | Node 24.18.0; pnpm 12.4.2 verified from the workspace Corepack cache. Package downloads still fail npm DNS.                                                                                    |
| Python / uv            | Managed Python 3.13.16 found; API .venv created with it. System Python 3.14.7; uv 0.13.4. Makefile no longer hides host-managed installs.                                                      |
| Pinned versions file   | docs/VERSIONS.md (installed tools distinguished from uninstalled direct pins)                                                                                                                  |
| Registry access        | npm, PyPI and files.pythonhosted.org downloads fail DNS. Cached registry metadata is sufficient for make lock, not package installation.                                                       |
| Git                    | No `.git` repository supplied; no commits created                                                                                                                                              |

## Phases

| Phase | Title                                                    | Status      | Date       | Notes                                                                                                                                                                                               |
| ----- | -------------------------------------------------------- | ----------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 01    | Bootstrap                                                | IN-PROGRESS | 2026-10-21 | Scaffolds, Compose, CI, tests, 11 ADRs and inventory written. Python/pnpm found; make lock passed for both ecosystems. Dependency downloads, generated contracts and runtime checks remain blocked. |
| 02    | Identity, hierarchy, operations, RBAC, audit foundation  | NOT-STARTED |            |                                                                                                                                                                                                     |
| 03    | Web shell, design system, auth UI                        | NOT-STARTED |            |                                                                                                                                                                                                     |
| 04    | Incidents backend                                        | NOT-STARTED |            |                                                                                                                                                                                                     |
| 05    | Realtime + incidents web UI (M1)                         | NOT-STARTED |            |                                                                                                                                                                                                     |
| 06    | Object storage, worker, attachments                      | NOT-STARTED |            |                                                                                                                                                                                                     |
| 07    | Geospatial backend + web map                             | NOT-STARTED |            |                                                                                                                                                                                                     |
| 08    | Agents, teams, devices, tracking, realtime map (M2)      | NOT-STARTED |            |                                                                                                                                                                                                     |
| 09    | Mobile shell, auth, map, tracking, online incidents (M3) | NOT-STARTED |            |                                                                                                                                                                                                     |
| 10    | Offline: SQLite, outbox, location buffer (M4)            | NOT-STARTED |            |                                                                                                                                                                                                     |
| 11    | Sync matrices, reports, dashboard                        | NOT-STARTED |            |                                                                                                                                                                                                     |
| 12    | Notifications, geofencing, history playback              | NOT-STARTED |            |                                                                                                                                                                                                     |
| 13    | Hardening: observability, load, security, privacy        | NOT-STARTED |            |                                                                                                                                                                                                     |
| 14    | Documentation, final validation (M5)                     | NOT-STARTED |            |                                                                                                                                                                                                     |

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
OBS-01 | AUTO | IN-PROGRESS | Logging/health/readiness source and tests written; runtime tests NOT RUN (L-111..112); metrics/OTel are Phase 13.
SEC-01 | AUTO | NOT-STARTED |
SEC-02 | AUTO | NOT-STARTED |
PERF-01 | AUTO | NOT-STARTED |
PERF-02 | MANUAL | NOT-STARTED |
DX-01 | AUTO | IN-PROGRESS | Real Python/JS locks validated by make lock; setup/verify fail downloading packages. Generated schemas remain absent (L-112..114).
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

## Decisions beyond DECISIONS.md

(date · phase · decision · reason — also create an ADR if architectural)

## Backlog (noticed, belongs to another phase)

- CORRECTED (2026-10-21, resume): AUTHZ-01..03 are present in SPEC.md and both inventories. The previous backlog claim that they were missing was incorrect; no requirement or Phase 02 implementation was added.
- Seed is an explicit NOT_IMPLEMENTED command until the Phase 02 domain model exists.
- API/worker metrics and OpenTelemetry remain Phase 13; bootstrap monitoring has no synthetic domain data.

## Blocked

- L-111 RESOLVED for Python discovery. Both lock files exist and make lock passes. L-110, L-112..114 remain: Docker socket unavailable, package downloads blocked, dependencies/contracts absent, native tooling unavailable.
- Resume Phase 01; do not start Phase 02 until exit checks pass.
- In a network-enabled environment: `make lock setup`, inspect Expo compatibility, `make infra-up migrate contracts`, then `make verify phase-check` and runtime smoke checks.
- Review `docs/VERSIONS.md` against installed versions; commit real locks/contracts only after generation.

## Human sign-offs

| Item | Who | Date | Device / env | Result |
| ---- | --- | ---- | ------------ | ------ |
