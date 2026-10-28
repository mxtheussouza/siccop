# AGENTS.md — Rules for every session

You are building the platform described in `SPEC.md`, using the decisions in `docs/DECISIONS.md`.
These rules apply to every phase and override convenience.

## 1. Session protocol

1. Read, in order: `AGENTS.md`, `docs/PROGRESS.md`, `docs/LIMITATIONS.md`, the phase prompt you were given, then only the `SPEC.md` / `DECISIONS.md` sections that phase references.
2. Inspect the repo before writing. Do not overwrite valid work. Do not redo finished phases.
3. Work **only on the current phase**. If you notice work belonging to another phase, add a line to `docs/PROGRESS.md` under "Backlog" and move on.
4. Do not ask the user for things you can do yourself (create files, run commands, fix errors). Ask only under the **Blocker rule** (section 6).
5. Finish by: running `make verify`, running the phase's own checks, updating `docs/PROGRESS.md` and `docs/LIMITATIONS.md`, and sending the **Session report** (section 8).

## 2. The single gate: `make verify`

Created in Phase 01 and extended every phase. It must run, in order, and fail on the first error:

```
format-check → lint → typecheck → unit tests → integration tests → build
```

for every project that exists (api, web, mobile, packages). A phase is **not done** until `make verify` exits 0 and you paste the tail of its output in the session report.

Forbidden ways to get green: disabling or loosening type checks or lint rules, deleting or skipping tests, `xfail` without a linked entry in `LIMITATIONS.md`, `# type: ignore` / `# pyright: ignore` / `@ts-ignore` / `any` without a one-line justification comment at the site, mocking the database in tests that claim to test PostgreSQL/PostGIS behavior, SQLite as a stand-in for PostGIS.

## 3. Honesty rules (most important)

- Every requirement in `SPEC.md` has an ID and a verification class in `docs/VERIFICATION.md`. You may only mark a requirement **DONE** if its class evidence exists:
  - `AUTO` → a passing automated test you can name.
  - `EMU` → a passing emulator/simulator/E2E run, or it stays `IMPLEMENTED-UNVERIFIED`.
  - `DEVICE` → code complete + manual checklist written. Status is **never above `IMPLEMENTED-UNVERIFIED`** until the human ticks the checklist.
- No fake features: no buttons without behavior, forms that only `console.log`, hardcoded arrays as repositories, fake auth, simulated GPS as final behavior, fake WebSocket, invented dashboard numbers, silently swallowed errors. Seed/demo data only in development.
- If something cannot be built or verified, implement up to the boundary, make the gap **visible in the product** (disabled control with reason, or HTTP 501 with code `NOT_IMPLEMENTED`), and list it in `docs/LIMITATIONS.md`. Never present it as working.
- Never claim performance or scalability numbers you did not measure. Record measured numbers with the command and environment used.
- Never claim you tested iOS if you did not run iOS. Say what ran where.

## 4. Engineering rules

**Language.** All identifiers, filenames, tables, columns, routes, events, config keys, logs and technical docs in English. End-user strings in pt-BR via an i18n catalog (never inline literals in components). No Portuguese in code (`incident`, not `incidente`).

**Backend (Python).** Python 3.13, FastAPI, Pydantic v2, SQLAlchemy 2.x async + asyncpg, Alembic, PostGIS via GeoAlchemy2. Modular monolith: modules under `apps/api/src/app/modules/<module>/` with only the layers that module needs (`domain/ application/ infrastructure/ presentation/`). No cross-module imports of another module's `infrastructure`; talk through its `application` API or domain events.
- Transaction boundary = one unit of work per request/command, committed by the application layer. Repositories never commit.
- API never returns ORM models. Explicit Pydantic schemas (`XCreate`, `XUpdate`, `XRead`, `XListItem`).
- Async only for I/O. CPU/blocking work (Shapely on large inputs, PDF, Pillow, boto3 sync calls, KML/KMZ parsing) goes to the worker or `anyio.to_thread`, never inline in the event loop.
- Timezone-aware datetimes only; UTC in storage.
- Errors use the format in `DECISIONS.md §Errors`. No stack traces in production responses.
- Logging: structlog, JSON, correlation ID on every line. **Never log raw coordinates, tokens, passwords or attachment URLs at INFO or above.**

**Database.** Alembic migrations only; never `create_all` outside tests. FKs, unique + check constraints, GiST on geometry, partial indexes where useful. Every operational table has `operation_id` (or a path to it) and every query is scoped by it.

**Authorization.** Enforced server-side in a single dependency/policy layer. Every endpoint has a test for: unauthenticated (401), wrong operation (403), insufficient role (403), allowed (2xx). The permission matrix lives in `SPEC.md §3`; do not scatter role checks.

**Web (Next.js).** TypeScript strict, App Router, TanStack Query owns server state, Zustand only for transient global UI state. Domain rules never live in the frontend. Every async view has loading / empty / error / success (and offline where relevant). WCAG AA target; severity never conveyed by color alone.

**Mobile (Expo).** TypeScript strict, Expo Router, development builds (not Expo Go-only). Every feature evaluated for Android **and** iOS (permissions, background behavior, lifecycle, safe areas, keyboard). Platform differences go behind an abstraction under `src/services/platform/`. Tokens in SecureStore. Mobile never decides domain rules; it only queues commands and shows server truth.

**API contracts.** FastAPI OpenAPI is authoritative. Generate TS types/client into `packages/contracts` (`make contracts`); CI fails if generated output is stale. Do not hand-duplicate types.

**Dependencies.** Pin versions per `DECISIONS.md §Versions`. Never `latest` in manifests. Check installed versions and docs before adapting to API changes.

**Secrets.** Nothing real in the repo. `.env.example` only. No signing credentials. Dev seed credentials are documented and refused when `APP_ENV=production`.

**Commits.** Small, conventional-commit messages, one logical change each. Never commit generated build output or secrets.

## 5. Definition of done (per task)

A task is done when: code + migration (if any) + tests (positive, negative, authorization) + docs touched + `make verify` green. UI tasks additionally need the five states and a pt-BR catalog entry.

## 6. Blocker rule

If a requirement is blocked (needs a device, macOS, a paid credential, an unavailable service, or a decision not covered by `DECISIONS.md`):

1. Pick the most conservative default consistent with `DECISIONS.md`.
2. Implement up to the boundary.
3. Record in `docs/LIMITATIONS.md`: requirement ID, what is missing, why, what a human must do.
4. Continue with unblocked work.

Stop and ask the user **only** if continuing would require an irreversible or security-relevant choice not covered by the docs (e.g., deleting data, choosing a legal basis, spending money).

## 7. Environment notes

- Docker may be unavailable. Detect it first (`docker info`). If missing, integration tests that need containers are marked and reported as **NOT RUN** (never silently skipped), and you say so in the report.
- iOS builds require macOS. On Linux you may typecheck, test shared logic and run `expo prebuild --no-install` checks, but you cannot claim an iOS build.
- Windows/macOS/Linux differences for `make` and shell scripts are documented in the README.

## 8. Session report (mandatory format)

```
## Session report — Phase NN
Done:           <requirement IDs with evidence: test names / commands>
Implemented but unverified: <IDs + why>
Stubs / limitations added: <IDs>
Not run (and why): <commands/tests>
make verify:    <last 15 lines of output>
Decisions taken beyond DECISIONS.md: <list or "none">
Next session should start with: <1–3 lines>
```

No celebratory summary. No recap of steps. If a check failed, say so first.
