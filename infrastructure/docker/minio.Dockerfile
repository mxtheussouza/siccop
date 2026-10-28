FROM minio/mc:RELEASE.2025-04-16T18-13-26Z AS client
FROM minio/minio:RELEASE.2025-04-22T22-12-26Z
COPY --from=client /usr/bin/mc /usr/bin/mc
