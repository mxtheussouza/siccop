# Phase 05 — Realtime + incidents web UI (Milestone M1)

**Objective:** authenticated WebSocket delivery with replay, and the incident screens on web working live across two browsers.

**Read:** SPEC §6 (RT-01..04, INC-08), event catalog; DECISIONS (Realtime: envelope, transactional outbox, Streams, tickets, catch-up, backpressure).

## Tasks

1. Outbox relay (worker or API background task with `FOR UPDATE SKIP LOCKED`) publishing to `ops:{id}:events` Redis Streams with `sequence`; marks `published_at`; at-least-once, metrics for lag.
2. `POST /api/v1/realtime/tickets` (single-use, 30 s, bound to user+operation) and `/ws/operations/{operation_id}`: validate ticket, check membership, replay from `last_event_id` or send `resync.required`, heartbeat, bounded per-connection queue, close codes (4403 revoked, 4408 slow consumer), max message 16 KB.
3. Membership/role/disable changes cause the gateway to re-check and close affected connections.
4. Web: `useOperationEvents` hook (ticket → connect → exponential-backoff reconnect with `last_event_id`; handle `resync.required` by invalidating TanStack Query caches); events patch/invalidate query caches (no polling).
5. Incident UI: `/operations/[id]/incidents` (virtualized table, filters, cursor pagination, live updates, highlight of changed rows), detail page (header, status, description, assignment, actions timeline, transitions timeline), create dialog, transition controls limited to the server-allowed next states (fetched from API), claim button with proper 409 handling (clear message showing who holds it), action form, optimistic locking conflict dialog. All five states on every view; pt-BR strings.
6. Connection status indicator in the top bar (connected / reconnecting / resyncing).

## Tests

- Backend integration: event appears in stream after commit and **not** if the transaction rolls back; duplicate relay publish is deduped by `event_id`; replay returns exactly the missed events; stale `last_event_id` → `resync.required`; client of operation A never receives operation B events (RT-03); revoked membership → connection closed 4403; ticket reuse rejected; expired ticket rejected.
- Web unit: hook reconnect/backoff and cache patching with a fake WebSocket server.
- Playwright: SCENARIO 2 with two browser contexts (operator creates incident → second client updates without refresh); claim race from two contexts → one succeeds, other sees the conflict message.

## Exit criteria

- `make verify` green.
- RT-01..03 AUTO evidence; RT-04, INC-08 EMU evidence (Playwright) or NOT RUN with reason.
- Milestone M1 demo script documented in README (steps a human can follow).

## Out of scope

Attachments, map, location events.
