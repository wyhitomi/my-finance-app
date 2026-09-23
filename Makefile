.DEFAULT_GOAL := help
API := apps/api
WEB := apps/web
OPENSPEC := OPENSPEC_TELEMETRY=0 npx -y @fission-ai/openspec@1.13.1

.PHONY: help setup hooks check test api-check web-check specs api-dev web-dev db-up db-down

help: ## List targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

setup: ## Install API and web dependencies and git hooks
	cd $(API) && uv sync
	cd $(WEB) && pnpm install --frozen-lockfile
	$(MAKE) hooks

hooks: ## Install pre-commit and commit-msg hooks
	uvx pre-commit install

check: api-check web-check specs ## Everything CI runs

test: ## Run all test suites
	cd $(API) && uv run pytest
	cd $(WEB) && pnpm test:coverage

api-check: ## Lint, typecheck, boundaries and tests for the API
	cd $(API) && uv run ruff format --check . && uv run ruff check . && uv run mypy && uv run lint-imports && uv run pytest

web-check: ## Lint, typecheck, tests and build for the web app
	cd $(WEB) && pnpm format:check && pnpm lint && pnpm typecheck && pnpm test:coverage && pnpm build

specs: ## Validate OpenSpec specs and changes
	$(OPENSPEC) validate --all --strict --no-interactive

api-dev: ## Run the API with reload on :8000
	cd $(API) && uv run uvicorn finance_api.main:app --reload

web-dev: ## Run the web app on :5173
	cd $(WEB) && pnpm dev

db-up: ## Start local PostgreSQL
	docker compose -f infra/docker-compose.yml up -d

db-down: ## Stop local PostgreSQL
	docker compose -f infra/docker-compose.yml down
