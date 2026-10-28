# Phase 06 — Object storage, worker, attachments

**Objective:** safe attachment pipeline for incidents/actions using S3-compatible storage and the Dramatiq worker.

**Read:** SPEC §4 (IncidentAttachment), §6 (ATT-01); DECISIONS (Backend stack: worker/storage/MIME/Pillow; Attachments).

## Tasks

1. Dramatiq worker app + Redis broker, retries with backoff, dead-letter handling, `make worker`, compose profile, worker failure metric hook. Middleware that propagates correlation ID.
2. Storage service (`aioboto3`/thread-isolated boto3): bucket bootstrap for MinIO, presigned PUT/GET (5 min), private bucket, key scheme from DECISIONS.
3. Migration + module `attachments`: declare → presigned upload → `complete` → worker job (sniff real MIME from bytes with libmagic, enforce size, compute sha256, generate thumbnail, HEIC→JPEG derivative, PDF allowed without rendering) → `READY` or `REJECTED` with reason. Download endpoint returns a presigned URL **only** for `READY` and only with incident read permission in that operation.
4. Events `incident.updated` (attachment added) via the outbox; audit entry on upload/rejection.
5. Web: attachment uploader on incident detail (drag/drop, progress, per-file status, retry, rejected state with reason), thumbnails grid, authorized download. Client-side image downscale before upload.
6. Orphan cleanup job: `PENDING_UPLOAD` older than 24 h removed from DB and storage.

## Tests

- MIME spoofing: a `.jpg` that is an executable/HTML is `REJECTED`; a real JPEG renamed `.txt` is accepted as JPEG; oversize rejected before/after upload; zero-byte rejected.
- Authorization: other-operation user cannot declare, complete or download; observer can download but not upload.
- Presigned URL expiry respected (short TTL test).
- Worker retries and idempotent re-processing; thumbnail created.
- Testcontainers MinIO integration.

## Exit criteria

- `make verify` green; ATT-01 AUTO evidence; web uploader works against MinIO (Playwright or documented manual run); mobile camera parts remain for Phase 09.

## Out of scope

Mobile capture UI.
