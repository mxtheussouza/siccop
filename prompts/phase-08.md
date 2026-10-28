# Phase 08 — Agents, teams, devices, tracking, realtime map (Milestone M2)

**Objective:** end-to-end location pipeline from a device-shaped client to the moving marker on the web map, with correct privacy controls.

**Read:** SPEC §4 (Team, Agent, Device, AgentLocation), §5 (Tracking state), §6 (AGT, TRK-01..06, TRK-09, PRIV-01, RT), event catalog; DECISIONS (Tracking, Realtime ephemeral events, Privacy).

## Tasks

Backend

1. Migrations: teams, agents, devices (hash of app install ID), `agent_locations` (monthly partitions + maintenance job), `agent_latest_location`, per-operation tracking policy in `operations.settings` with the DECISIONS defaults and validation.
2. CRUD for teams/agents/devices, agent↔team, device registration/revocation (revoked device cannot ingest), agent status updates (`agent.status.updated`).
3. `POST …/tracking/locations/batch`: all validations from DECISIONS (limits, future timestamps, accuracy, device↔agent↔operation association, membership), per-point result, `ON CONFLICT DO NOTHING` dedupe, skew correction, latest-location upsert only if newer, Redis latest state, ephemeral `agent.location.updated` publish after commit. Rate limit per device. **No raw coordinates in INFO logs.**
4. Tracking state derivation (LIVE/STALE/OFFLINE) returned in agent payloads using the policy; endpoint returning the policy to clients.
5. History endpoint (bounded window/points, downsampling, cursor) with CHIEF+ authorization and an audit event per access (agent, window, no coordinates). Retention job dropping expired partitions.
6. `tools/sim-device`: clearly labeled **development tool** that authenticates as an agent and posts realistic paths (walk/drive), supports offline bursts and out-of-order/duplicate points to exercise the pipeline. It is a test harness, not product behavior.

Web 7. Agents list/detail (`/operations/[id]/agents[/agentId]`) and teams page: search, filters (team, status, tracking state), team/agent management for CHIEF+. 8. Map: agent layer with team/status/tracking-state styling (icon + text in tooltip, not color alone), incremental `setData` with ≤ 4 Hz throttling, clustering, snapshot on (re)connect, follow-agent mode, agent details panel, filters.

## Tests

- Ingest: valid batch; duplicates (resend same batch → all `duplicate`); out-of-order; future timestamp; clock-skew adjustment flag; bad coordinates; huge batch/payload; revoked device; wrong operation; observer role cannot ingest as another agent.
- Latest-location monotonicity under concurrent batches.
- Partition creation + retention drop (real PostgreSQL).
- History: bounds, downsampling, authz (OPERATOR → 403), audit row written.
- WS: location events reach only members of that operation; reconnect gets snapshot, not replay.
- Playwright (EMU): SCENARIO 3/4 pipeline using `tools/sim-device` → marker moves in browser. SCENARIO 10 (history path) at API level now, UI in Phase 12.
- Log test: capture logs during ingest; assert no coordinates at INFO+.

## Exit criteria

- `make verify` green.
- AGT-01, TRK-01..05, TRK-09, TRK-06 (EMU part), RT location isolation updated with evidence. `[D]` parts of TRK-06 stay `IMPLEMENTED-UNVERIFIED`.
- Milestone M2 demo script in README: start sim-device, watch marker move, draw an area, create incident from map.

## Out of scope

Real mobile app, geofencing, playback UI.
