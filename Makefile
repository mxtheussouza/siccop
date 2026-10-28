SHELL := /bin/sh
.DEFAULT_GOAL := help
.NOTPARALLEL:

export UV_CACHE_DIR ?= $(CURDIR)/.cache/uv
# Preserve uv's managed-runtime discovery; a project install directory hides host installs.
export COREPACK_HOME ?= $(CURDIR)/.cache/corepack
API := uv run --locked --project apps/api
COMPOSE := docker compose --env-file .env

.PHONY: help lock setup infra-up infra-down migrate seed api web worker mobile mobile-dev test test-integration lint format format-check typecheck build contracts contracts-check verify phase-check

help:
	@echo 'Read README.md for setup, environment requirements and the Phase 01 boundary.'
	@echo 'Main gate: make verify (format → lint → types → unit → integration → build)'

lock:
	uv lock --project apps/api
	pnpm install --lockfile-only

setup:
	python3 tools/bootstrap.py
	uv sync --locked --project apps/api
	pnpm install --frozen-lockfile
	pnpm --filter @platform/mobile exec expo install --check

infra-up:
	$(COMPOSE) up -d --wait --wait-timeout 180

infra-down:
	$(COMPOSE) down

migrate:
	cd apps/api && uv run --locked alembic upgrade head

seed:
	$(API) python -m app.seed

api:
	$(API) uvicorn app.main:create_app --factory --env-file .env --host 127.0.0.1 --port 8000 --no-access-log

web:
	node --env-file-if-exists=.env tools/run.mjs pnpm --filter @platform/web dev

worker:
	$(API) dramatiq app.worker --processes 1 --threads 4 --skip-logging

mobile:
	node --env-file-if-exists=.env tools/run.mjs pnpm --filter @platform/mobile build

mobile-dev:
	node --env-file-if-exists=.env tools/run.mjs pnpm --filter @platform/mobile dev

test:
	$(API) pytest apps/api/tests/unit --cov=app --cov-report=term-missing
	pnpm -r test
	python3 -m unittest discover -s tools/tests -v

test-integration:
	python3 tools/check_docker.py
	$(API) pytest apps/api/tests/integration -m integration -v

lint:
	$(API) ruff check --config apps/api/pyproject.toml apps/api tools
	pnpm lint

format:
	$(API) ruff format --config apps/api/pyproject.toml apps/api tools
	pnpm format

format-check:
	$(API) ruff format --check --config apps/api/pyproject.toml apps/api tools
	pnpm format-check

typecheck:
	$(API) pyright --project apps/api
	pnpm typecheck

build:
	uv build --project apps/api --out-dir apps/api/dist
	node --env-file-if-exists=.env tools/run.mjs pnpm build

contracts:
	pnpm --filter @platform/contracts generate

contracts-check:
	pnpm --filter @platform/contracts check

verify:
	$(MAKE) format-check
	$(MAKE) lint
	$(MAKE) typecheck
	$(MAKE) test
	$(MAKE) test-integration
	$(MAKE) build
	$(MAKE) contracts-check

phase-check:
	python3 tools/check_phase.py
	$(MAKE) contracts-check
	pnpm --filter @platform/mobile config-check
