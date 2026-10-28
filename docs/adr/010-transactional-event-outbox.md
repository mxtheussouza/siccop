# ADR-010: Transactional domain event outbox

Status: accepted in DECISIONS.md.

## Context

Publishing directly to Redis during an incident transaction can announce a rolled-back change, or miss a committed change if the process fails between commit and publish.

## Decision

Insert durable domain events in PostgreSQL in the same unit of work as the mutation. A worker relay reads with `FOR UPDATE SKIP LOCKED`, publishes to operation Streams and records publication. Delivery is at least once; consumers deduplicate by event ID and compare entity versions. High-rate location updates follow the separate ephemeral policy.

## Alternatives

Direct post-commit publishing has a crash window. Distributed two-phase commit would couple database and broker availability. Full event sourcing would change the data model and introduce replay complexity not required by the specification.

## Consequences

Duplicate publication is expected and tested. Relay lag and failures require metrics and operational monitoring later. Phase 02 creates the table; Phase 05 implements relay behavior. No event relay is claimed in Phase 01.
