# ADR-009: Same-origin web and rotating refresh sessions

Status: accepted in DECISIONS.md.

## Context

Web and native clients have different secure storage and CSRF boundaries. Stolen refresh tokens must be revocable without exposing reusable tokens to URL logs or browser persistent storage.

## Decision

Use same-origin web API proxying. Web access tokens stay in memory, with rotating opaque refresh tokens in HttpOnly, Secure, SameSite=Strict cookies scoped to the auth route. Check Origin/Host on cookie-authenticated commands. Mobile receives refresh tokens in the body and stores them in SecureStore. Reuse revokes the refresh family; token_version supports access-token revocation.

## Alternatives

Browser localStorage simplifies reloads but exposes persistent tokens to injected scripts. Long-lived JWT refresh tokens complicate server revocation. Cross-origin cookies add browser policy and CSRF complexity.

## Consequences

Page load needs a refresh bootstrap; family rotation and concurrent reuse need integration tests. Token storage must be tested on physical devices before DEVICE evidence is accepted. Phase 01 has no credential collection or fake auth; server auth begins in Phase 02.
