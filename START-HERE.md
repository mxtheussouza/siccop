# Agent Pack — Situational Awareness Platform

This pack replaces the single monolithic prompt. Copy its contents to the **root of the new repository**, commit, then drive the agent **one phase per session**.

## Layout

```
AGENTS.md                 Rules the agent must always follow (code, quality, honesty, blockers)
SPEC.md                   Product + domain: entities, roles, state machines, requirements with IDs
docs/DECISIONS.md         Decisions already taken (stack, protocols, policies). Do not re-litigate.
docs/VERIFICATION.md      What can be verified by machine vs. device vs. manual, per requirement
docs/PROGRESS.md          Agent's memory between sessions (updated every session)
docs/LIMITATIONS.md       Declared stubs, unverifiable items, blocked items
prompts/_session.md       Preamble to paste at the start of EVERY session
prompts/phase-01..14.md   One prompt per phase, each with objective exit criteria
```

## How to run

1. Put the Pacificador manual (if you want functional parity) at `docs/reference/pacificador-manual.pdf`. If absent, the agent uses `SPEC.md` only and must not invent behavior beyond it.
2. Start a session. Paste `prompts/_session.md`, replacing `NN` with the phase number.
3. The agent works until the phase exit criteria pass (`make verify` green + phase checks), updates `docs/PROGRESS.md`, and stops.
4. Review the diff and `docs/LIMITATIONS.md`. Commit. Start the next phase in a **fresh session**.

## Milestones

| Milestone | After phase | What you can demo |
|---|---|---|
| M1 — Web + API vertical | 05 | Login, operations, incidents, capture, realtime in two browsers |
| M2 — Map + tracking | 08 | POIs/routes/areas, imports, simulated agent moving on web map |
| M3 — Mobile online | 09 | Android/iOS app: login, map, GPS, incidents (device checklist required) |
| M4 — Offline | 10 | Outbox + location buffer + reconciliation |
| M5 — Complete | 14 | Everything in `SPEC.md`, with honest `LIMITATIONS.md` |

## Why modular

- Smaller context per session → no silent degradation of late phases.
- Decisions are written once (`DECISIONS.md`) → no arbitrary choices per session.
- `PROGRESS.md` + `make verify` → objective state instead of self-reported success.
- `VERIFICATION.md` → the agent cannot mark device-only features as "done".
