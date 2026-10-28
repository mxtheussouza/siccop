# Phase 01 — Bootstrap

**Objective:** a monorepo where every project boots, with one verification gate, infrastructure, pinned versions and decision records. No domain features yet.

**Read:** SPEC §1, §6 (DX-01); DECISIONS (Versions, Backend stack, ADR list); VERIFICATION (probe).

## Tasks

1. Probe the environment (VERIFICATION.md) and record results in `docs/PROGRESS.md → Environment`.
2. Create the monorepo layout from the original structure: `apps/{api,web,mobile}`, `packages/{contracts,types,config,tooling}`, `infrastructure/{docker,nginx,monitoring,scripts}`, `docs/{architecture,database,api,mobile,security,adr}`, `.github/workflows`, `tools/` (for dev scripts such as `sim-device`).
3. `docker-compose.yml`: PostGIS, Redis, MinIO (+ bucket bootstrap), optional profiles `worker`, `monitoring` (Prometheus, Grafana). Healthchecks on all. `.env.example` with every variable (no real secrets).
4. `apps/api`: `uv` project, FastAPI app factory, config via `pydantic-settings`, structlog JSON logging with correlation-ID middleware, `/health` and `/ready` (checks DB, Redis, storage), Alembic initialized with the PostGIS extension migration, Ruff + Pyright strict + pytest + coverage configured, module skeleton directories for all modules in SPEC (empty `__init__.py` only), error handler producing the DECISIONS error format. One real test per layer proving wiring (health endpoint, error format, config loading).
5. `apps/web`: Next.js App Router, TypeScript strict, Tailwind, shadcn/ui initialized, TanStack Query provider, i18n scaffolding with `pt-BR` catalog, Vitest + Testing Library configured, a real `/login` placeholder page that is clearly marked as not yet wired (not a fake login).
6. `apps/mobile`: Expo (SDK from VERSIONS) + Expo Router + TypeScript strict, `app.config.ts`, `eas.json` with `development|preview|production` for `android` and `ios` (no credentials), Jest configured, tabs skeleton labeled Mapa/Incidentes/Operação/Alertas/Perfil with non-functional-state screens clearly marked "not implemented yet" (these are skeleton routes, not features).
7. `packages/contracts`: script that exports OpenAPI from the API and generates TS types (`make contracts`); CI check that generated output is up to date.
8. `Makefile` with: `setup infra-up infra-down migrate seed api web worker mobile test test-integration lint format format-check typecheck build contracts verify`. Document Windows/macOS/Linux notes in README (WSL recommendation for Windows).
9. `make verify` implemented exactly as in AGENTS.md §2 and green.
10. GitHub Actions: `api.yml` (ruff, pyright, pytest with services), `web.yml`, `mobile.yml` (lint, typecheck, tests), plus `security.yml` (dependency audit, gitleaks). No signing credentials.
11. `docs/VERSIONS.md` with the pinned versions actually installed.
12. Create ADR-001…011 from DECISIONS.md with real trade-offs (Context / Decision / Alternatives / Consequences).
13. Create `docs/PROGRESS.md` full requirement table (every SPEC requirement ID, status `NOT-STARTED`) and README with quickstart.

## Exit criteria (all must pass)

- `make infra-up` → all containers healthy (if Docker available; else reported NOT RUN).
- `make api` serves `/health` 200 and `/ready` 200 with infra up; `/ready` returns 503 when Redis is stopped (test or manual evidence).
- `make web` builds and serves `/login` placeholder; `make mobile` produces a bundle (`expo export` or equivalent) without errors.
- `make verify` exits 0.
- OpenAPI export + generated TS types committed and `make contracts` leaves no diff.
- ADR-001…011 exist; `docs/VERSIONS.md` exists; PROGRESS requirement table complete.
- No `any`, `@ts-ignore` or pyright ignores without justification comments.

## Out of scope

Any domain entity, authentication, real screens.
