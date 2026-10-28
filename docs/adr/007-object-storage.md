# ADR-007: Private S3-compatible object storage

Status: accepted in DECISIONS.md.

## Context

Incident attachments and import files need durable binary storage without putting large payloads in relational rows or proxying every upload through the API process.

## Decision

Use private S3-compatible storage, MinIO locally. Authorize metadata actions in the API and issue short-lived presigned URLs. A worker verifies bytes, size, MIME and derivatives before downloads become available. Keys are operation-scoped. Synchronous SDK calls run in a thread or worker.

## Alternatives

Database blobs simplify atomic metadata ownership but burden database backups and I/O. A shared filesystem requires deployment-specific scaling and access controls. Public buckets remove URL issuance but would expose sensitive incident attachments.

## Consequences

Uploads have an explicit lifecycle and orphan cleanup is needed later. Storage readiness verifies the configured bucket, not only a TCP connection. Phase 01 provisions a private bucket; attachment API and processing arrive in Phase 06.
