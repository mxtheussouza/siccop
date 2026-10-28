# ADR-005: Operation-scoped WebSocket protocol

Status: accepted in DECISIONS.md.

## Context

Operators must see authorized updates without refreshing. Reconnection, slow consumers and authorization changes must be explicit protocol cases, and long-lived tokens must stay out of URLs.

## Decision

Use an authenticated REST request to issue a one-use, 30-second ticket bound to user, operation and IP hash. WebSocket connections subscribe to one operation. Use the fixed event envelope, bounded queues, heartbeat, replay by event ID and `resync.required` when the retained window is exceeded. Re-check membership changes and close unauthorized connections.

## Alternatives

Polling is simpler but adds repeated queries and update latency. SSE fits one-way traffic but does not match the chosen heartbeat and connection protocol. Access tokens in URLs can leak through URL logs and history.

## Consequences

Clients must deduplicate and refetch newer entity versions. Queue overflow is a visible reconnect/resync condition rather than unbounded memory growth. Phase 05 implements this ADR; Phase 01 contains no simulated WebSocket or global event feed.
