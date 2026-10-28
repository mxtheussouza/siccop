# Android device verification

Requirements: AUTH-05, ATT-02, TRK-06, TRK-07, NOT-02, OFF-04; related UX MOB-04. Status: NOT-STARTED. This is a future-phase checklist, not evidence of implemented features. Only a human tester may tick items after running the relevant build on a physical device.

| Tester  | Date | Device | OS version | Build ID | Result  | Notes            |
| ------- | ---- | ------ | ---------- | -------- | ------- | ---------------- |
| Pending | —    | —      | —          | —        | NOT RUN | No device tested |

- [ ] SecureStore persists tokens across the supported app lifecycle; logout removes them; no plaintext token storage/logging.
- [ ] Foreground location rationale appears before the OS prompt; denial remains usable.
- [ ] Background permission is requested separately with rationale; denial preserves foreground-only behavior.
- [ ] Foreground service notification remains visible while background tracking is active.
- [ ] Screen locked for 30 minutes: authorized points arrive in the server; record measured counts and device policy.
- [ ] Airplane mode for 10 minutes: fixes are buffered; reconnect uploads each accepted point once.
- [ ] Doze and battery-saver behavior is recorded for this device/OS.
- [ ] Camera and gallery use separate permission paths; denial/limited access remain usable; compression is verified.
- [ ] Push arrives in foreground, background and terminated states; record OS-specific restrictions.
- [ ] Create an incident and action offline; reconnect; exactly one server record exists for each command.
- [ ] Back navigation works on each screen; edge-to-edge insets and keyboard do not obscure controls.
- [ ] 200% font scaling, small/large phone layouts and tablet layout remain usable.

Emulator checks, JS bundles and native build logs must be recorded separately; they cannot tick physical-device results.
