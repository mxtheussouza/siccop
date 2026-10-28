# Version record

Recorded 2026-10-21. **The application dependencies below are exact proposed pins, not installed or verified packages.** Both real lock files are now present and `make lock` passes using cached metadata. Registry DNS still blocks package downloads and installation. On resume, Python 3.13.16 was found and its discovery was fixed in the Makefile. Do not describe this table as a resolved dependency tree.

## Observed tools

| Tool | Installed result |
|---|---|
| OS | Darwin 27.0.0 arm64 (macOS) |
| Node | 24.18.0 (LTS major 24; `.nvmrc`) |
| uv | 0.13.4 |
| Python | Managed CPython 3.13.16 verified; API .venv uses it. System Python remains 3.14.7. |
| Docker CLI / Compose | 29.8.0 / 5.5.1; daemon unavailable |
| pnpm | 12.4.2 verified from the workspace Corepack cache on the second resume |
| Xcode / Android | Full native toolchains and simulators unavailable |

## Runtime and package pins awaiting installation

Python 3.13.16 is selected in `.python-version` and is now verified at the host uv-managed path. The Makefile no longer overrides `UV_PYTHON_INSTALL_DIR`, so uv discovers that installed runtime; project caches remain local. Application dependencies are still not installed. pnpm 12.4.2 is pinned in the root manifest and its cached executable now runs successfully. Python dependencies require `apps/api/uv.lock`; JS dependencies require root `pnpm-lock.yaml`. **Both locks exist and were validated by `make lock` on the second resume (2026-10-21).** uv resolved 86 packages; pnpm validated all 7 workspace projects. Installation still fails on uncached package downloads. Lock metadata is not proof of installed packages; update this file from actual installations after `make setup` passes.

The bootstrap checked [Next.js registry metadata](https://registry.npmjs.org/next/latest) (16.4.2), [Expo registry metadata](https://registry.npmjs.org/expo/latest) (58.0.16), and Expo's [SDK 58 native compatibility map](https://raw.githubusercontent.com/expo/expo/sdk-58/packages/expo/bundledNativeModules.json). React 19.3.0 and React Native 0.88.0 match that map. Native installation through `expo install` and compatibility checks remain NOT RUN. The [Next.js October security update](https://nextjs.org/blog/nextjs-security-update-october-14-2026) identifies the patched 16.4 line. These are registry observations, not local build evidence.

FastAPI 0.156.4, SQLAlchemy 2.1.5 and pydantic-settings 2.16.1 were checked against their publisher metadata on PyPI; Pydantic 2.14.1 and Uvicorn 0.54.0 were also observed in the local uv cache. No API dependency was installed into this checkout. Other direct pins are conservative explicit candidates and still require resolver and audit checks.

### API

| Dependency | Pin | Installation |
|---|---|---|
| fastapi (runtime) | 0.156.4 | NOT INSTALLED |
| pydantic (runtime) | 2.14.1 | NOT INSTALLED |
| pydantic-settings (runtime) | 2.16.1 | NOT INSTALLED |
| uvicorn (runtime) | 0.54.0 | NOT INSTALLED |
| sqlalchemy[asyncio] (runtime) | 2.1.5 | NOT INSTALLED |
| asyncpg (runtime) | 0.30.0 | NOT INSTALLED |
| alembic (runtime) | 1.15.2 | NOT INSTALLED |
| geoalchemy2 (runtime) | 0.17.1 | NOT INSTALLED |
| redis (runtime) | 5.2.1 | NOT INSTALLED |
| boto3 (runtime) | 1.38.13 | NOT INSTALLED |
| structlog (runtime) | 25.3.0 | NOT INSTALLED |
| dramatiq[redis] (runtime) | 1.18.0 | NOT INSTALLED |
| ruff (development) | 0.11.8 | NOT INSTALLED |
| pyright (development) | 1.1.400 | NOT INSTALLED |
| pytest (development) | 8.3.5 | NOT INSTALLED |
| pytest-asyncio (development) | 0.26.0 | NOT INSTALLED |
| pytest-cov (development) | 6.1.1 | NOT INSTALLED |
| httpx (development) | 0.28.1 | NOT INSTALLED |
| testcontainers[postgres,redis,minio] (development) | 4.10.0 | NOT INSTALLED |
| boto3-stubs[s3] (development) | 1.38.13 | NOT INSTALLED |
| pip-audit (development) | 2.9.0 | NOT INSTALLED |

### JavaScript workspaces

The exact direct pins are listed below; transitive versions are recorded in the real lock files, but those packages are not installed or verified.

| Workspace | Dependency | Pin |
|---|---|---|
| operational-platform | @eslint/js | 9.39.1 |
| operational-platform | @types/node | 24.10.1 |
| operational-platform | eslint | 9.39.1 |
| operational-platform | eslint-plugin-react-hooks | 7.0.1 |
| operational-platform | globals | 16.5.0 |
| operational-platform | prettier | 3.6.2 |
| operational-platform | typescript | 5.9.3 |
| operational-platform | typescript-eslint | 8.46.4 |
| @platform/mobile | expo | 58.0.16 |
| @platform/mobile | expo-constants | 58.0.12 |
| @platform/mobile | expo-dev-client | 58.0.14 |
| @platform/mobile | expo-linking | 58.0.13 |
| @platform/mobile | expo-router | 58.0.24 |
| @platform/mobile | expo-status-bar | 58.0.3 |
| @platform/mobile | react | 19.3.0 |
| @platform/mobile | react-native | 0.88.0 |
| @platform/mobile | react-native-safe-area-context | 5.10.1 |
| @platform/mobile | react-native-screens | 4.30.0 |
| @platform/mobile | @testing-library/react-native | 13.3.3 |
| @platform/mobile | @types/jest | 29.5.14 |
| @platform/mobile | @types/react | 19.3.0 |
| @platform/mobile | babel-preset-expo | 58.0.18 |
| @platform/mobile | jest | 29.7.0 |
| @platform/mobile | jest-expo | 58.0.11 |
| @platform/mobile | react-test-renderer | 19.3.0 |
| @platform/web | @tanstack/react-query | 5.90.5 |
| @platform/web | class-variance-authority | 0.7.1 |
| @platform/web | clsx | 2.1.1 |
| @platform/web | next | 16.4.2 |
| @platform/web | react | 19.3.0 |
| @platform/web | react-dom | 19.3.0 |
| @platform/web | tailwind-merge | 3.3.1 |
| @platform/web | @tailwindcss/postcss | 4.1.16 |
| @platform/web | @testing-library/jest-dom | 6.9.1 |
| @platform/web | @testing-library/react | 16.3.0 |
| @platform/web | @types/react | 19.3.0 |
| @platform/web | @types/react-dom | 19.3.0 |
| @platform/web | jsdom | 27.1.0 |
| @platform/web | tailwindcss | 4.1.16 |
| @platform/web | vitest | 3.2.7 |
| @platform/contracts | openapi-fetch | 0.15.0 |
| @platform/contracts | openapi-typescript | 7.10.1 |

## Container pins (not pulled or verified)

| Component | Image |
|---|---|
| PostGIS | `postgis/postgis:17-3.5` (required version line; mutable publisher tag, not a digest) |
| Redis | `redis:7.4.2-alpine` |
| MinIO server | `minio/minio:RELEASE.2025-04-22T22-12-26Z` |
| MinIO client | `minio/mc:RELEASE.2025-04-16T18-13-26Z` |
| Prometheus | `prom/prometheus:v3.3.0` |
| Grafana | `grafana/grafana:11.6.1` |
| API base | `python:3.13.16-slim` |
| uv builder | `ghcr.io/astral-sh/uv:0.13.4` |
| CI gitleaks | `zricethezav/gitleaks:v8.24.2` |

Image availability, architecture support and scans remain unverified. Do not claim immutable container reproducibility until publisher digests have been resolved in a network-enabled session.
