# Version record

Refreshed 2026-10-28 (UTC) from an actual installation on the host below. Every version listed
here was installed by `make setup` from the committed lock files (`apps/api/uv.lock`,
`pnpm-lock.yaml`) and exercised by a green `make verify`. Transitive versions live in the locks.

## Toolchain (observed)

| Tool                  | Version                           | Notes                                                   |
| --------------------- | --------------------------------- | ------------------------------------------------------- |
| OS                    | Ubuntu 26.04 LTS on WSL2 (x86_64) | Kernel 6.6.87.2-microsoft-standard-WSL2                 |
| Node                  | 24.18.0                           | Official tarball, SHA-256 verified; `.nvmrc`            |
| pnpm                  | 12.4.2                            | Via Corepack (`packageManager`)                         |
| uv                    | 0.13.4                            | Official installer                                      |
| Python (API)          | 3.13.16                           | uv-managed; system Python 3.14 is not used by the API   |
| Docker Engine/Compose | 29.5.1 / 5.1.3                    | Daemon reachable                                        |
| Expo SDK              | 58 (`expo` 58.0.20)               | `expo install --check`: dependencies up to date         |
| Android SDK / Xcode   | not installed                     | No native build or emulator/simulator run (L-114/L-103) |

## API (Python, exact pins in `apps/api/pyproject.toml`)

| Dependency          | Installed | Group       |
| ------------------- | --------- | ----------- |
| fastapi             | 0.156.4   | runtime     |
| starlette           | 1.9.0     | transitive  |
| pydantic            | 2.14.1    | runtime     |
| pydantic-settings   | 2.16.1    | runtime     |
| uvicorn             | 0.54.0    | runtime     |
| sqlalchemy[asyncio] | 2.1.5     | runtime     |
| asyncpg             | 0.30.0    | runtime     |
| alembic             | 1.15.2    | runtime     |
| geoalchemy2         | 0.17.1    | runtime     |
| redis               | 5.2.1     | runtime     |
| boto3               | 1.38.13   | runtime     |
| structlog           | 25.3.0    | runtime     |
| dramatiq[redis]     | 1.18.0    | runtime     |
| ruff                | 0.11.8    | development |
| pyright             | 1.1.400   | development |
| pytest              | 9.0.3     | development |
| pytest-asyncio      | 1.4.1     | development |
| pytest-cov          | 6.1.1     | development |
| httpx               | 0.28.1    | development |
| testcontainers      | 4.10.0    | development |
| boto3-stubs[s3]     | 1.38.13   | development |
| pip-audit           | 2.9.0     | development |

pytest 8.3.5 → 9.0.3 and pytest-asyncio 0.26.0 → 1.4.1 on 2026-10-28 to fix PYSEC-2026-1845.

## JavaScript workspaces (exact pins in each `package.json`)

| Workspace           | Dependency                         | Installed        |
| ------------------- | ---------------------------------- | ---------------- |
| root                | typescript                         | 6.0.3            |
| root                | typescript-eslint                  | 8.72.1           |
| root                | eslint / @eslint/js                | 9.39.1           |
| root                | eslint-plugin-react-hooks          | 7.0.1            |
| root                | prettier                           | 3.6.2            |
| root                | @types/node                        | 24.10.1          |
| root                | globals                            | 16.5.0           |
| @platform/web       | next                               | 16.4.2           |
| @platform/web       | react / react-dom                  | 19.3.0           |
| @platform/web       | @tanstack/react-query              | 5.90.5           |
| @platform/web       | tailwindcss / @tailwindcss/postcss | 4.1.16           |
| @platform/web       | class-variance-authority           | 0.7.1            |
| @platform/web       | clsx                               | 2.1.1            |
| @platform/web       | tailwind-merge                     | 3.3.1            |
| @platform/web       | vitest                             | 4.1.12           |
| @platform/web       | jsdom                              | 27.1.0           |
| @platform/web       | @testing-library/react             | 16.3.0           |
| @platform/web       | @testing-library/jest-dom          | 6.9.1            |
| @platform/mobile    | expo                               | 58.0.20          |
| @platform/mobile    | expo-router                        | 58.0.27          |
| @platform/mobile    | expo-constants                     | 58.0.13          |
| @platform/mobile    | expo-dev-client                    | 58.0.16          |
| @platform/mobile    | expo-linking                       | 58.0.14          |
| @platform/mobile    | expo-status-bar                    | 58.0.4           |
| @platform/mobile    | react-native                       | 0.88.0           |
| @platform/mobile    | react-native-safe-area-context     | 5.10.1           |
| @platform/mobile    | react-native-screens               | 4.30.0           |
| @platform/mobile    | babel-preset-expo                  | 58.0.18          |
| @platform/mobile    | jest / jest-expo                   | 30.5.2 / 58.0.12 |
| @platform/mobile    | @testing-library/react-native      | 14.1.0           |
| @platform/mobile    | test-renderer                      | 1.3.1            |
| @platform/contracts | openapi-typescript                 | 7.10.1           |
| @platform/contracts | openapi-fetch                      | 0.15.0           |
| @platform/contracts | typescript                         | 5.9.3            |

Changes on 2026-10-28, all driven by tool output:

- Expo packages raised to the patches required by `expo install --check` (SDK 58).
- TypeScript 5.9.3 → 6.0.3: Next 16.4.2 declarations reference `URLPattern*` types that only
  TypeScript 6 `lib.dom` provides. typescript-eslint 8.46.4 → 8.72.1 for TS 6 support.
- `@platform/contracts` keeps TypeScript 5.9.3 because `openapi-typescript` peers on `^5.x`.
- vitest 3.2.7 → 4.1.12 for GHSA advisories in vitest/@vitest/mocker/tinypool.
- @testing-library/react-native 13.3.3 → 14.1.0 (peer required by expo-router 58.0.27);
  `react-test-renderer` replaced by its peer `test-renderer`.

## Containers (pulled and healthy on 2026-10-28)

| Component         | Image                                                 | Observed runtime                                                            |
| ----------------- | ----------------------------------------------------- | --------------------------------------------------------------------------- |
| PostGIS           | `postgis/postgis:17-3.5`                              | PostgreSQL 17.5, PostGIS 3.5.2                                              |
| Redis             | `redis:7.4.2-alpine`                                  | 7.4.2                                                                       |
| MinIO server + mc | `bitnamilegacy/minio:2025.4.22@sha256:50cec18a…6da01` | MinIO RELEASE.2025-04-22T22-12-26Z, mc RELEASE.2025-04-16T18-13-26Z (L-123) |
| Prometheus        | `prom/prometheus:v3.3.0`                              | healthy (monitoring profile)                                                |
| Grafana           | `grafana/grafana:11.6.1`                              | healthy (monitoring profile)                                                |
| API / worker base | `python:3.13.16-slim` + `ghcr.io/astral-sh/uv:0.13.4` | worker profile healthy                                                      |
| CI gitleaks       | `zricethezav/gitleaks:v8.24.2`                        | ran locally: no leaks                                                       |

`minio/minio` and `minio/mc` are no longer published on Docker Hub (pull returns "repository does
not exist"); the archived Bitnami build contains the same MinIO and mc commits. Only the MinIO
image is digest-pinned; the others use publisher tags.
