# Phase 07 — Geospatial backend + web operational map

**Objective:** map workspace with base layers, POIs, routes, areas, imported layers, geospatial queries, filters and clustering — all persisted and live.

**Read:** SPEC §4 (POI, Route, OperationalArea, MapLayer, GeospatialImport), §6 (GEO-01..07), event catalog; DECISIONS (Web map, Imports security, Errors).

## Tasks

Backend
1. Migrations + CRUD (with `version` locking, validation, authz per matrix, audit, outbox events `poi|route|area.*`, `layer.*`).
2. Geometry validation: coordinate range, `ST_IsValid`, vertex/size caps, Polygon/MultiPolygon only for areas, LineString for routes.
3. Geospatial query module (PostGIS only): `incidents in bbox`, `objects inside area`, `agents within radius` and `nearest N agents` (against `agent_latest_location`, table created now with no writers yet), `tracks intersecting area` (query implemented; data arrives in Phase 08). GiST indexes; bbox endpoints bounded (max features, simplification by zoom for imported features).
4. Import pipeline per DECISIONS: presigned upload → worker validation/parsing (defusedxml, KMZ limits, byte sniffing, feature caps, ignore NetworkLinks) → `GeospatialImport`, `MapLayer`, `imported_feature`; deletion cascades; status polling + `layer.created` event.

Web
5. `/operations/[id]/map`: MapLibre with configured base layers (street/satellite/topographic/hybrid shown only if configured), layer visibility panel, fit bounds, fullscreen, current location, object selection with details panel, context menu on long-press/right-click ("Create incident here", "Create POI here"), filters (incident type/priority/status/assignment; POIs/routes/areas/imports) updating without reload.
6. Drawing/editing via Terra Draw for POI, route, area with save/cancel and server validation errors shown; permission-aware (observer sees no drawing tools).
7. Clustering for incidents and POIs (agents get it in Phase 08), click-to-expand; incremental source updates from realtime events (no layer recreation); bbox-driven loading for large layers.
8. Import UI: upload, status, layer list, delete.

## Tests

- Geometry validation (invalid polygons, bow-ties, out-of-range, oversize).
- PostGIS queries with fixture data across operations; **EXPLAIN assertions** for GiST use; isolation between operations.
- Import security: XXE payload, billion-laughs, zip bomb (ratio), path traversal entries, > cap features, NetworkLink (must not fetch — assert no outbound call), spoofed extension, valid KML/KMZ/GeoJSON round trip.
- Authz matrix rows for all new endpoints.
- Web: unit tests for filter state → query params; Playwright: draw a POI/route/area and see it persist after reload and appear live in a second browser; create incident from map context action.

## Exit criteria

- `make verify` green.
- GEO-01..06 evidence (AUTO/EMU); GEO-07 documented with a config example and the "layer hidden when unconfigured" behavior tested.
- Map interaction stays responsive with a seeded dataset of 5,000 incidents/POIs (record frame behavior qualitatively and the dataset size; no invented FPS numbers).

## Out of scope

Agent markers and tracking (Phase 08), mobile.
