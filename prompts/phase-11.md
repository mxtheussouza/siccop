# Phase 11 — Synchronization matrices, reports, dashboard

**Objective:** operational planning timeline, real reports from data, and a dashboard built only from real aggregates.

**Read:** SPEC §4 (Synchronization*, SituationReport), §5 (Sync action machine), §6 (SYN, REP, DASH-01), event catalog (`sync.action.*`); DECISIONS (worker, Errors).

## Tasks

Backend
1. Migrations + CRUD: matrices and actions (version locking), status state machine, clone (deep copy, optional date shift), filters, events `sync.action.created|updated|status_changed`, audit entries. "Overdue" flag derived at read time, never auto-changing status.
2. Situation reports: DRAFT editing; FINALIZE computes `content_sha256`, locks the row (DB trigger or constraint preventing updates), audit event; amend = new report with `supersedes_id`.
3. Reports from SQL (no Python-side bulk aggregation): incident report, incident history (transitions + actions), agent activity (counts/time-in-state from tracking and status history), operational timeline (union of incidents, actions, sync actions, transitions), situation report. Parameters bounded (window caps). CSV streaming export; PDF generation as a **worker job** (status polling, signed download) for large reports.
4. Dashboard aggregates endpoint: active agents, online agents (tracking state LIVE), open incidents, critical incidents, incidents by status, recent activity — computed in SQL, cached briefly in Redis (invalidate by events), operation-scoped.

Web
5. `/operations/[id]/synchronization`: timeline (virtualized, zoom by day/hour), inspect panel, create/edit/delete/clone, status changes, filters; live updates.
6. `/operations/[id]/reports`: report picker with parameters, preview, CSV/PDF export with progress; situation report editor (draft autosave, finalize confirmation, read-only after finalization, supersede flow).
7. `/dashboard` and operation overview: real aggregates, compact map (reuse map component with incidents/agents), recent incidents list, operational timeline; EmptyState when no data. **No invented charts or numbers**; charts must be derived from the aggregates endpoint with accessible text alternatives.

## Tests

- State machine and authz matrix rows for sync endpoints; clone correctness.
- Finalized report immutable (API and direct DB update attempt fails); hash stable.
- Report SQL correctness against a known fixture dataset (assert exact counts/rows); operation isolation; bounded windows; query-count assertions; large dataset smoke (e.g., 100k incident_actions) completes within a recorded time on the test environment (record, don't promise).
- PDF job lifecycle; CSV streaming memory bounded (no full materialization).
- Web unit + Playwright: create matrix/actions, change status, second browser updates; finalize a situation report and confirm it becomes read-only.
- Dashboard numbers equal direct SQL counts in a test.

## Exit criteria

- `make verify` green.
- SYN-01/02, REP-01..03, DASH-01 evidence recorded.

## Out of scope

Notifications, geofencing, playback UI.
