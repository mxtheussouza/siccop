# VERIFICATION.md — What counts as evidence

The agent may run in an environment without Docker, full native toolchains, emulators, or physical devices. Detect the actual OS and capabilities; the Phase 01 probe found macOS arm64 with Command Line Tools only. This file defines what "done" may mean per requirement class so that nothing unverifiable is reported as verified.

## Classes

| Class | Meaning | Evidence required for DONE | Highest status without that evidence |
|---|---|---|---|
| `AUTO` | Deterministic code/logic | A named, passing automated test (unit/integration/contract). `make verify` green. | `IMPLEMENTED-UNVERIFIED` |
| `EMU` | Needs a running stack/UI/emulator but no real hardware | A passing Playwright/Maestro/scripted E2E run, with the command and output tail in the report | `IMPLEMENTED-UNVERIFIED` |
| `DEVICE` | Needs a real Android and/or iOS device (background GPS, push, camera, permissions UX) | A manual checklist in `docs/mobile/*.md` with each item **ticked by a human** (name + date + device + OS version) | `IMPLEMENTED-UNVERIFIED` |
| `MANUAL` | Design/doc/judgment review | Human sign-off in `docs/PROGRESS.md` | `IMPLEMENTED-UNVERIFIED` |

Status vocabulary (use exactly these): `NOT-STARTED`, `IN-PROGRESS`, `IMPLEMENTED-UNVERIFIED`, `DONE`, `BLOCKED`, `STUBBED`.

The agent may set `DONE` only when the class evidence exists. Everything else is reported honestly.

## Environment capability probe (Phase 01, re-run when in doubt)

Agent records results in `docs/PROGRESS.md → Environment`:

```
docker info                 # containers available?
uname -a                    # Linux/macOS
which adb emulator xcrun    # Android SDK / iOS tooling present?
node -v && pnpm -v && python3 --version && uv --version
```

Consequences:
- No Docker → Testcontainers/integration suites: **NOT RUN**, listed in report; provide `make test-integration` for the human.
- No macOS → no iOS build. Mobile iOS work is limited to config correctness (`app.config.ts`, `Info.plist` keys via config), shared-logic tests, TypeScript typecheck. iOS EMU/DEVICE items stay `IMPLEMENTED-UNVERIFIED`.
- No emulator → Maestro flows written and linted but **NOT RUN**.

## Matrix of the original end-to-end scenarios

| # | Scenario | Class | How verified |
|---|---|---|---|
| 1 | Admin creates operation, assigns users, operator accesses | AUTO + EMU | API integration test + Playwright |
| 2 | Operator creates incident, second web client receives event | EMU | Playwright with two browser contexts |
| 3 | Android GPS → API → PostGIS → web marker moves | AUTO (ingest→WS) + EMU (simulated device script) + **DEVICE** (real Android) | script `tools/sim-device` for the first two; checklist for the third |
| 4 | Same with iOS | AUTO + EMU + **DEVICE** (real iPhone) | same; iOS device checklist |
| 5 | Operator assigns incident → mobile receives it | AUTO (event) + EMU (emulator) + DEVICE | |
| 6 | Android offline → action → reconnect → synced once | AUTO (outbox logic, idempotency) + EMU (Maestro on emulator, airplane mode) + DEVICE | |
| 7 | Same on iOS | AUTO + DEVICE (simulator is EMU if macOS) | |
| 8 | Two operators capture same incident | AUTO | ≥ 20 concurrent claims on real PostgreSQL → exactly 1 success |
| 9 | Unauthorized access → 403 | AUTO | per-endpoint authz tests |
| 10 | Location history → path displayed | AUTO (query) + EMU (UI) | |

## Manual device checklists (agent writes them; humans tick them)

Files: `docs/mobile/android.md`, `docs/mobile/ios.md`. Each has the sections below with `- [ ]` items and a result table (tester, date, device, OS version, build id, pass/fail, notes).

Android:
- [ ] Foreground permission prompt shows rationale first; denial path usable
- [ ] Background permission requested separately, with rationale; denial keeps foreground tracking only
- [ ] Foreground service notification visible while tracking in background
- [ ] Tracking continues with screen off for 30 min; points arrive (check server count)
- [ ] Airplane mode 10 min → points buffered → reconnect → all synced once
- [ ] Doze / battery saver behavior documented
- [ ] Camera + gallery attach; permissions separate
- [ ] Push notification received foreground/background/killed
- [ ] System back behavior on every screen; edge-to-edge insets; keyboard doesn't hide inputs; 200% font scale usable
- [ ] Phone small/large + tablet layouts

iOS:
- [ ] When-In-Use prompt with correct usage description; "Always" upgrade flow with rationale
- [ ] Background location indicator appears; tracking continues locked screen 30 min
- [ ] App killed by user → documented behavior (no tracking until reopen unless significant-change configured)
- [ ] Airplane mode buffer → reconnect → synced once
- [ ] Camera + photo library separate prompts (limited library access handled)
- [ ] Push notification foreground/background/killed
- [ ] Safe areas on notch/Dynamic Island devices; keyboard avoidance; swipe-back; Dynamic Type max size
- [ ] iPhone small/large + iPad layouts

## Reporting rule

In every Session report, list per requirement ID: status + evidence (test name / command / checklist ref). A report claiming `DONE` for a `DEVICE` item without a ticked checklist is invalid and must be corrected.

## Complete requirement classification (Phase 01 inventory)

Expanded from SPEC.md. Composite classes require all listed evidence; they are not alternatives. Status and test evidence live in PROGRESS.md.

| Requirement | Verification classes |
|---|---|
| AUTHZ-01 | AUTO |
| AUTHZ-02 | AUTO |
| AUTHZ-03 | AUTO |
| AUTH-01 | AUTO |
| AUTH-02 | AUTO |
| AUTH-03 | AUTO |
| AUTH-04 | AUTO |
| AUTH-05 | EMU + DEVICE |
| AUTH-06 | MANUAL |
| ADM-01 | AUTO |
| ADM-02 | AUTO |
| ADM-03 | AUTO |
| ADM-04 | AUTO |
| ADM-05 | AUTO |
| OPS-01 | AUTO |
| OPS-02 | EMU |
| INC-01 | AUTO |
| INC-02 | AUTO |
| INC-03 | AUTO |
| INC-04 | AUTO |
| INC-05 | AUTO |
| INC-06 | AUTO |
| INC-07 | AUTO |
| INC-08 | EMU |
| ATT-01 | AUTO |
| ATT-02 | DEVICE |
| GEO-01 | AUTO |
| GEO-02 | AUTO |
| GEO-03 | AUTO |
| GEO-04 | EMU |
| GEO-05 | EMU |
| GEO-06 | EMU |
| GEO-07 | MANUAL |
| AGT-01 | AUTO |
| TRK-01 | AUTO |
| TRK-02 | AUTO |
| TRK-03 | AUTO |
| TRK-04 | AUTO |
| TRK-05 | AUTO |
| TRK-06 | EMU + DEVICE |
| TRK-07 | DEVICE |
| TRK-08 | DEVICE |
| TRK-09 | AUTO |
| TRK-10 | EMU |
| PRIV-01 | MANUAL |
| RT-01 | AUTO |
| RT-02 | AUTO |
| RT-03 | AUTO |
| RT-04 | EMU |
| SYN-01 | AUTO |
| SYN-02 | EMU |
| REP-01 | AUTO |
| REP-02 | AUTO |
| REP-03 | AUTO |
| DASH-01 | EMU |
| AUD-01 | AUTO |
| AUD-02 | EMU |
| NOT-01 | AUTO |
| NOT-02 | DEVICE |
| GEF-01 | AUTO |
| MOB-01 | EMU |
| MOB-02 | EMU |
| MOB-03 | EMU |
| MOB-04 | MANUAL |
| MOB-05 | AUTO |
| OFF-01 | AUTO |
| OFF-02 | AUTO |
| OFF-03 | AUTO |
| OFF-04 | EMU + DEVICE |
| OBS-01 | AUTO |
| SEC-01 | AUTO |
| SEC-02 | AUTO |
| PERF-01 | AUTO |
| PERF-02 | MANUAL |
| DX-01 | AUTO |
| DOC-01 | MANUAL |
