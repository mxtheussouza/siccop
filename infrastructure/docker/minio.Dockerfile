# MinIO no longer publishes community images. This archived build is the same MinIO
# (RELEASE.2025-04-22T22-12-26Z) and mc (RELEASE.2025-04-16T18-13-26Z) commits, digest-pinned.
# Development/test only; it receives no security updates (LIMITATIONS L-123).
FROM bitnamilegacy/minio:2025.4.22@sha256:50cec18ac4184af4671a78aedd5554942c8ae105d51a465fa82037949046da01
ENTRYPOINT ["minio"]
