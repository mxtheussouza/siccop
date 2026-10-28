# Phase 03 — Web shell, design system, auth UI

**Objective:** a real, authenticated web application shell with a design system, operation selector and admin basics. No fake data anywhere.

**Read:** SPEC §6 (AUTH-05, OPS-02, ADM), §3; DECISIONS (Authentication topology, Web map not yet); AGENTS §4 (Web).

## Tasks

1. Design tokens (spacing, typography, radius, elevation, semantic status colors, component states) with light and dark themes. Components: Button, Input, Select, Dialog, Sheet, Drawer, Card, Table (virtualized), Badge, Tooltip, Tabs, Timeline, EmptyState, ErrorState, LoadingState, Skeleton, StatusIndicator, PriorityIndicator. `StatusIndicator`/`PriorityIndicator` must convey meaning with **icon + text**, not color alone.
2. App shell: collapsible sidebar, top command bar, responsive behavior (desktop/tablet/mobile-web fallback), theme switch.
3. Auth: `/login` wired to the real API; in-memory access token; refresh bootstrap on page load via the HttpOnly cookie; automatic refresh before expiry; logout; protected routes; expired-session handling. Verify nothing is written to localStorage/sessionStorage.
4. Operation selector: `/operations` lists the user's operations (from API), selecting one sets context for `/operations/[operationId]/…`; non-member URL → 403 page. Role-aware navigation (items hidden by server-provided permissions, never by client-only role guesses; server remains the authority).
5. `/dashboard` shell showing **only** real data that exists now (e.g., list of operations) or an EmptyState; no placeholder charts.
6. `/admin/users`, `/admin/organizations`, `/admin/command-centers`, `/admin/operations` with working CRUD forms (React Hook Form + Zod), membership management on the operation page, and optimistic UI only where safe.
7. All strings via the pt-BR catalog; accessibility pass (focus order, labels, contrast, keyboard) on shell and forms.
8. Typed API client generated from OpenAPI used throughout (no hand-written duplicate types).

## Tests

- Vitest + Testing Library: forms validation, permission-based rendering, error/empty/loading states, token never persisted to storage (assert).
- Playwright (against dev stack; if it cannot run, mark NOT RUN): SCENARIO 1 — admin logs in, creates operation, adds a member, operator logs in and sees the operation; observer cannot see admin routes.

## Exit criteria

- `make verify` green (web lint, typecheck, tests, build).
- Playwright scenario 1 passing, or explicitly NOT RUN with reason and the command to run.
- axe (or equivalent) automated check on login, shell, admin list pages: zero serious/critical violations.
- AUTH-05 (web part), OPS-02, ADM UI items updated in PROGRESS with evidence.

## Out of scope

Map, incidents, mobile screens.
