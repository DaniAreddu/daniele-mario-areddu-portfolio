SHELL := /bin/sh
.DEFAULT_GOAL := help

## Show available targets.
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

## Start the full development stack (db, backend, frontend, mailpit, gateway).
dev:
	docker compose up --build

## Start the development stack in the background.
up:
	docker compose up --build -d

## Stop and remove the development stack's containers.
down:
	docker compose down

## Tail logs from every service.
logs:
	docker compose logs -f

## Apply database migrations inside the backend container.
migrate:
	docker compose exec backend uv run alembic upgrade head

## Run the idempotent content seed inside the backend container.
seed:
	docker compose exec backend uv run python -m app.seed.seed

## Run backend and frontend automated tests.
test: test-backend test-frontend

test-backend:
	docker compose exec backend uv run pytest

test-frontend:
	docker compose exec frontend npm run test

## Run backend and frontend linters.
lint: lint-backend lint-frontend

lint-backend:
	docker compose exec backend uv run ruff check .

lint-frontend:
	docker compose exec frontend npm run lint

## Run backend and frontend type checkers.
typecheck: typecheck-backend typecheck-frontend

typecheck-backend:
	docker compose exec backend uv run mypy app

typecheck-frontend:
	docker compose exec frontend npm run typecheck

## Build production images for every service.
build:
	docker compose -f docker-compose.prod.yml build

## Open a shell in the backend container.
shell-backend:
	docker compose exec backend sh

## Open a shell in the frontend container.
shell-frontend:
	docker compose exec frontend sh

## Back up the PostgreSQL database to backup.sql.
db-backup:
	docker compose exec -T db pg_dump -U $${POSTGRES_USER:-portfolio} $${POSTGRES_DB:-portfolio} > backup.sql

## Restore the PostgreSQL database from backup.sql.
db-restore:
	cat backup.sql | docker compose exec -T db psql -U $${POSTGRES_USER:-portfolio} $${POSTGRES_DB:-portfolio}

.PHONY: help dev up down logs migrate seed test test-backend test-frontend lint lint-backend lint-frontend typecheck typecheck-backend typecheck-frontend build shell-backend shell-frontend db-backup db-restore
