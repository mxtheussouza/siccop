# Phase 14 — Documentation, final validation (Milestone M5)

**Objective:** a developer can clone and run the entire system from the docs, and every claim in the docs matches reality. Final honest audit of status.

**Read:** SPEC §9, VERIFICATION (scenario matrix), PROGRESS, LIMITATIONS.

## Tasks

1. Docs complete and accurate: `README.md` (quickstart, commands, Windows/macOS/Linux notes, dev credentials marked dev-only), `CONTRIBUTING.md`, `docs/architecture/{overview,backend,realtime,mobile,offline}.md`, `docs/database/schema.md` (generated from the live schema where possible), `docs/security/security-model.md`, `docs/mobile/{android,ios}.md`, `docs/api/README.md` (+ link to OpenAPI), ADR-001…011 reviewed against what was actually built (update, don't leave aspirational text).
2. Mermaid diagrams (rendered check): system architecture, domain relationships, realtime flow, GPS tracking flow, mobile offline sync flow, incident lifecycle.
3. Fresh-clone validation: in a clean directory, follow README step by step: `.env` → `make infra-up migrate seed` → api/web/worker → mobile bundle. Fix every doc or script defect found. Record the transcript summary.
4. Execute the full E2E suite for SCENARIOS 1–10 to the extent possible; produce `docs/VALIDATION.md` with a row per scenario: class, what ran, where (OS/emulator/device), result, evidence link. Items needing devices are listed as **pending human checklist**, not passed.
5. Definition-of-done walk (SPEC §9): each bullet marked verified/unverified with evidence.
6. Final audit: reconcile `docs/PROGRESS.md` requirement table with reality (downgrade anything unsupported by evidence), reconcile `docs/LIMITATIONS.md`, ensure every disabled/stubbed UI element corresponds to an entry, ensure no TODO/FIXME/fake data paths remain in production code (grep gate in `make verify`), ensure seed credentials are refused under `APP_ENV=production` (test).
7. Release hygiene: version tags, changelog, `eas.json` profiles documented, no secrets in history (gitleaks full scan).

## Exit criteria

- `make verify` green on a fresh clone; CI green.
- `docs/VALIDATION.md` complete and honest; PROGRESS requirement table consistent with it.
- Every `DEVICE` requirement is either ticked by a human (with name/date/device/OS) or listed as `UNVERIFIED-ON-DEVICE`.
- Final report lists: DONE count, IMPLEMENTED-UNVERIFIED count with reasons, STUBBED/BLOCKED with who must act.
