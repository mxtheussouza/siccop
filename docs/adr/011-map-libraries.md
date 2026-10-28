# ADR-011: MapLibre and Terra Draw

Status: accepted in DECISIONS.md.

## Context

The platform needs interactive vector maps, editable operational objects and frequent location updates across web and native clients. Base layers must be replaceable without embedding production provider credentials.

## Decision

Use MapLibre GL JS with Terra Draw on web and MapLibre React Native in mobile development builds. Styles and optional base layers are configured externally. Throttle incremental GeoJSON source updates; do not rebuild layers on each location event. Drawing is web-only in v1.

## Alternatives

Raster-focused libraries simplify a basic map but need additional work for frequent vector updates. A proprietary mapping SDK could simplify provider integration but changes licensing, costs and key management. Expo Go-only mapping would constrain the selected native library.

## Consequences

Native compatibility with the pinned Expo SDK must be verified in Phase 09; a fallback requires a new ADR if needed. Missing provider configurations hide optional layers. Public OSM servers are not a production default. Phase 01 contains no map dependency, tiles, tracking simulation or rendered operational features.
