# Phase 10 — Offline: SQLite, outbox, location buffer, reconciliation (Milestone M4)

**Objective:** the mobile app keeps working without connectivity and converges to server truth exactly once, with honest sync status.

**Read:** SPEC §5 (Outbox), §6 (OFF-01..04, MOB-05, TRK location buffer), DECISIONS (Offline — commands table, outbox rules, conflict policy, location buffer; Tracking dedupe/clock skew).

## Tasks

1. SQLite schema + migrations (versioned, forward-only) for `cached_operation`, `cached_incident`, `cached_assignment`, `cached_map_object`, `pending_command` (id, idempotency_key, operation_id, command_type, payload, depends_on, created_at, attempt_count, last_attempt_at, next_attempt_at, status, error_code, error_detail), `pending_location` (client_point_id, payload, recorded_at, synced_at). Transactions for every multi-row write.
2. Read-through caches: operations, incidents (assigned + nearby), assignments, map objects; stale-while-revalidate; "last synced at" per dataset; cache invalidated by realtime events and resync.
3. Outbox processor: strict FIFO per operation, `depends_on`, `Idempotency-Key` header, backoff with jitter, transient vs permanent classification exactly per DECISIONS, resumes after app kill (PROCESSING rows reset to PENDING at startup), single-flight (no concurrent processors), triggered by reconnect, foreground, timer, and manual "Sync now".
4. Supported offline commands only: `incident.create`, `incident.action.create`, `incident.attachment.upload`, `incident.transition.request`. Other actions show a clear "requires connection" state. Local IDs are the final UUIDs; reconcile `reference_number` from the server response.
5. Conflict handling: `FAILED` rows with server state shown; user can retry, edit, or discard (cascade to dependents with confirmation). Nothing silently overwritten.
6. Location buffer: write-ahead to `pending_location` **before** any network attempt; batch to server; remove/mark only per-point acknowledged ids (`accepted` or `duplicate`); bounded buffer with the DECISIONS eviction rule and visible eviction counter; survives app kill and reboot.
7. Network/sync status component, always visible: Online / Offline / Synchronizing (n) / Sync error (n). Counts read from SQLite. Never shows "synced" while any PENDING/PROCESSING/FAILED exists. Use `expo-network` plus request-failure detection (reachability is not trusted alone).
8. Attachments offline: photos stored in app sandbox (FileSystem), uploaded after parent create is synchronized; storage cleanup after success; disk-full handling.
9. Backend support if missing: idempotency on all four commands, `expected_from_status` conflict response `STATE_CONFLICT`, per-point acks.
10. Docs: `docs/architecture/offline.md` with Mermaid sequence diagrams (offline create → reconnect → sync; conflict; location buffer).

## Tests (Jest + real SQLite in Node, plus backend integration)

- Outbox: ordering, dependencies, retry/backoff schedule (fake timers), exactly-once under duplicate delivery (server returns original response for same key), crash between send and local ack (resend → server dedupes → local marks SYNCHRONIZED), PROCESSING recovery, FAILED classification, discard cascade.
- Location buffer: write-ahead ordering, partial batch acks, eviction policy, restart persistence, duplicate acks.
- Status component: all four states derived correctly from DB snapshots.
- Backend: replayed idempotent create/action → one row; transition with stale `expected_from_status` → 409 `STATE_CONFLICT`.
- Property/fuzz test for the outbox state machine (random failures/restarts → invariant: no duplicate server records, no lost commands).
- Maestro (EMU if emulator available): airplane mode → create incident + action → reconnect → exactly one of each on server. SCENARIO 6/7 DEVICE checklist items added to docs/mobile.

## Exit criteria

- `make verify` green (backend + mobile).
- OFF-01..03, MOB-05 AUTO evidence (named tests). OFF-04 EMU evidence or NOT RUN; `[D]` parts `IMPLEMENTED-UNVERIFIED` until human checklists are ticked on Android and iOS.

## Out of scope

Offline map tiles, offline claim/assign, multi-device conflict UI beyond the policy above.
