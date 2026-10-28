# iOS device verification

Requirements: AUTH-05, ATT-02, TRK-06, TRK-08, NOT-02, OFF-04; related UX MOB-04. Status: NOT-STARTED. This is a future-phase checklist, not evidence of implemented features. Only a human tester may tick items after running the relevant build on a physical device.

| Tester | Date | Device | OS version | Build ID | Result | Notes |
|---|---|---|---|---|---|---|
| Pending | — | — | — | — | NOT RUN | No device tested |

- [ ] SecureStore lifecycle and logout removal work; no plaintext token storage/logging.
- [ ] When-In-Use prompt has the correct usage explanation and prior rationale; denial remains usable.
- [ ] Always upgrade is requested separately with rationale, only when tracking needs it.
- [ ] Background indicator appears and authorized fixes arrive while the screen is locked for 30 minutes; record measured counts.
- [ ] User termination behavior is documented; no continued tracking is claimed without verified OS support.
- [ ] Airplane mode buffers fixes; reconnect uploads each accepted point once.
- [ ] Camera and library prompts are separate; limited photo access and denial remain usable; compression is verified.
- [ ] Push arrives in foreground, background and terminated states; record OS-specific restrictions.
- [ ] Create an incident and action offline; reconnect; exactly one server record exists for each command.
- [ ] Notch/Dynamic Island safe areas, keyboard avoidance and swipe-back work.
- [ ] Maximum Dynamic Type, small/large iPhone layouts and iPad layout remain usable.

Simulator checks, JS bundles and native build logs must be recorded separately; they cannot tick physical-device results. Full Xcode/simulator is absent in the current macOS environment.
