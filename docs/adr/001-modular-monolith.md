# ADR-001: Modular monolith

Status: accepted in DECISIONS.md; implementation starts in Phase 01.

## Context

Operations, incidents, assignments and audit need consistent transactions. A small platform team must be able to test and deploy the whole application without operating a distributed service mesh.

## Decision

Use a modular monolith under `apps/api/src/app/modules`. Create only the layers each module needs. Cross-module collaboration uses application APIs or domain events; infrastructure imports across modules are forbidden. One command/request owns a unit of work, committed in the application layer.

## Alternatives

Microservices provide independent deployment but introduce network failures and distributed consistency before there is evidence those costs are needed. A single unstructured package reduces initial ceremony but makes authorization and data ownership difficult to preserve.

## Consequences

Transactions remain local and refactoring is simpler. Module boundaries require review and tests; directories alone do not enforce them. Independently scaling a module would require a later extraction. Phase 01 creates empty module packages, not domain implementations.
