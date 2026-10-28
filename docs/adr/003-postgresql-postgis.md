# ADR-003: PostgreSQL and PostGIS

Status: accepted in DECISIONS.md.

## Context

Capture concurrency, operation isolation and spatial queries need one transactional source of truth. Location histories have different growth and retention characteristics from current entity state.

## Decision

Use PostgreSQL 17 with PostGIS 3.5. Apply schema changes only through Alembic. Scope operational queries by operation; constrain data with FKs, uniqueness and checks. Use GiST for spatial indexes. Later tracking history is partitioned monthly by recorded time; retention drops eligible partitions.

## Alternatives

SQLite does not provide PostGIS semantics or comparable concurrency and cannot substitute in integration tests. Separate document/spatial databases add consistency boundaries. Unpartitioned history simplifies initial writes but makes retention more expensive as history grows.

## Consequences

Integration tests require real PostgreSQL/PostGIS. Partition maintenance and retention become explicit operational duties in Phase 08. Phase 01 only enables the extension; downgrading that migration preserves the extension to avoid deleting shared spatial data.
