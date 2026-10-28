# Phase 09 — Mobile shell, auth, map, tracking, online incidents (Milestone M3)

**Objective:** Expo app for Android **and** iOS that logs in, selects an operation, shows the map, tracks location per policy, and works with incidents while online. Offline comes in Phase 10, but the architecture must not block it.

**Read:** SPEC §6 (MOB-01..04, TRK-07, TRK-08, ATT-02, PRIV-01, AUTH-05), §3; DECISIONS (Authentication topology/mobile, Mobile map, Tracking, Privacy); VERIFICATION (device checklists, environment probe); AGENTS §4 (Mobile).

## Tasks

1. Feature-oriented structure from the brief (`src/app`, `features/{auth,operations,map,tracking,incidents,teams,notifications,profile}`, `services/platform`, `database`, `providers`, `theme`). Shared design tokens aligned with web; platform-adaptive behavior behind `services/platform` (safe areas, back handling, haptics, status bar, modals, bottom sheets).
2. Auth: login against the real API with `X-Client: mobile`, refresh token in SecureStore, silent refresh, reuse-detection handling (forced re-login), logout wipes SecureStore and local caches. Operation selection screen (Operação tab).
3. Map tab: `@maplibre/maplibre-react-native` (development build), own position, assigned/nearby incidents, POIs, routes, areas, imported layers (read-only), clustering, layer/filter sheet, center-on-me, new-incident action (current location or map-picked), tracking status chip.
4. Tracking (foreground + background) with Expo Location + TaskManager, policy fetched from `/operations/{id}/tracking-policy`: min interval/distance, accuracy tiers, battery-aware. Separate **permission flows**: rationale screen → foreground prompt → separate rationale → background prompt (Android 10+/iOS Always). Android foreground service notification text; iOS background mode and `Info.plist` strings configured in `app.config.ts` only as needed. Persistent tracking indicator (PRIV-01). Send in batches to the batch endpoint with `client_point_id`; for now, failures keep points in a simple durable queue that Phase 10 will formalize (write-ahead to SQLite already, see below).
5. Incidents tab: cards (priority icon+text, status, distance, assignment, relative time), filters, detail with header/status/map/description/assignment/actions/attachments/timeline, create flow (location → type → priority → description → attachments), action registration, server-allowed transitions only. Bottom sheets. Camera and photo library via ImagePicker with **separate** permission handling; compress before upload; upload through the Phase 06 pipeline.
6. Alerts tab: in-app notification list fed by realtime (`notification.created`, incident assignment events); push registration deferred to Phase 12 but permission is **not** requested at launch.
7. Profile tab: user, role per operation, device registration status, tracking toggle (if policy allows), logout, app version.
8. Realtime on mobile: ticket + WebSocket with reconnect/catch-up, same envelope handling as web; pause on background, resume on foreground.
9. Accessibility: labels, roles, font scaling to 200 %, touch targets ≥ 44 pt/48 dp, severity never by color alone. Tablet: adaptive two-pane layouts for incidents and map where practical.
10. `app.config.ts`/`eas.json` complete for development/preview/production on both platforms; `docs/mobile/android.md` and `docs/mobile/ios.md`: setup, emulator/simulator/physical device commands, required permissions/manifest/Info.plist keys, limitations, and the device checklists from VERIFICATION.md.

## Tests

- Jest: auth state machine, token refresh/reuse handling, permission-flow state machine (all branches incl. denied/blocked/limited), tracking policy application, location batching/dedupe ids, incident form validation, API client error mapping.
- `npx tsc --noEmit`, lint, `expo-doctor`, `expo export` for **both** platforms must pass; `npx expo prebuild --no-install --platform android` (and ios when macOS) config validation.
- Maestro flows written for: login → select operation → open map → create incident; run on an emulator **if available**, else NOT RUN.

## Exit criteria

- `make verify` green (mobile lint/typecheck/tests/export).
- MOB-01..03 EMU evidence or `IMPLEMENTED-UNVERIFIED` with the exact missing environment.
- TRK-07, TRK-08, ATT-02 are `IMPLEMENTED-UNVERIFIED` unless the human ticked the checklists. Do **not** claim iOS was tested if only Linux was available.
- LIMITATIONS updated with every device/OS gap.

## Out of scope

Offline outbox, push, geofencing, mobile map-object drawing.
