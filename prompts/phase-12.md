# Phase 12 — Notifications, geofencing, history playback

**Objective:** in-app + push notifications, geofence events without storms, and bounded history playback on the web map.

**Read:** SPEC §4 (Notification, Geofence\*), §6 (NOT-01/02, GEF-01, TRK-10, TRK-04), event catalog; DECISIONS (Tracking: geofencing, history; Realtime).

## Tasks

Backend

1. Notifications: persisted per user/operation, created by domain events (critical incident created, assignment to my team/agent, incident status change on my claimed incident, sync action delayed, geofence events for subscribed roles). Fan-out in the worker; `notification.created` over WS; read/unread/read-all endpoints; per-user preferences.
2. Push: device `push_token` registration endpoint; Expo Push API client (httpx) in the worker with receipts handling (invalid token → device marked), retries; **no credentials in repo** (config only).
3. Geofencing per DECISIONS: evaluate latest accepted point per agent per batch with `ST_Covers` against geofence-enabled areas; Redis state + PG state; hysteresis; cooldown; ignore stale replayed points (>5 min) for events; emit `geofence.entered|exited` through the outbox; notifications for CHIEF/OPERATOR.
4. History playback API: bounded window, downsampling, optional `step`/time bucketing, returns timeline-friendly structure (LineString + timestamped points); already CHIEF+ and audited.

Web 5. Notification center (bell, unread count, list, mark read, preferences) driven by realtime. 6. Area editor: geofence toggle + cooldown; geofence events appear on map/timeline. 7. Playback UI in agent detail and map: select agent + window, render path, controls play/pause/seek/speed, timeline scrubber, bounded loading (windowed fetch while scrubbing), clear messages when truncated/downsampled.

Mobile 8. Contextual notification permission request (after the user opens Alerts or enables alerts — **never at launch**), token registration per OS (Android channel configuration, iOS permission model), notification handling foreground/background/tap deep-link to incident. Document in `docs/mobile/*.md`; add device checklist items.

## Tests

- Notification fan-out rules; idempotent creation per event; read/unread; WS delivery isolation.
- Geofence: enter/exit sequences, jitter at boundary (hysteresis), rapid in-out-in (cooldown) → bounded events, replayed old points produce no events, concurrent batches → single event, multi-area overlaps.
- Push client with HTTP mocked at the boundary (httpx transport) for success, invalid token, rate limit retry.
- Playback API bounds/downsampling/authz/audit; web unit tests for the playback controller (seek/speed/play state machine); Playwright SCENARIO 10: sim-device path → history → path displayed.

## Exit criteria

- `make verify` green.
- NOT-01, GEF-01, TRK-04, TRK-10 evidence; NOT-02 `IMPLEMENTED-UNVERIFIED` until device checklist ticked (also needs EAS/Firebase/APNs credentials → LIMITATIONS).

## Out of scope

SMS/email notifications, per-geofence custom rules.
