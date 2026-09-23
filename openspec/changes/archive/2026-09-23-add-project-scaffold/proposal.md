# Proposal

## Why

The repository has decisions (ADRs) and a spec workflow, but no runnable code.
Every feature (accounts, cards, budgets, reports, auth) needs the same foundation:
a modular FastAPI backend, a React SPA, i18n, the `Money` value object, test
tooling, pre-commit hooks and CI/CD. Building it once, test-first, lets later
changes focus on domain behavior.

## What Changes

- Monorepo layout `apps/api`, `apps/web`, `infra/` (ADR-0012).
- FastAPI app factory with `/api/v1/health`, versioned router and OpenAPI at `/api/openapi.json` (ADR-0002).
- Empty bounded-context packages (`identity`, `accounts`, `ledger`, `budgeting`, `reporting`) plus `shared_kernel`, with import-linter contracts enforcing boundaries (ADR-0004).
- `Money`/`Currency` value objects in the shared kernel (ADR-0007).
- Locale negotiation and localized error envelope in the API; react-i18next in the SPA with pt-BR/en-US and a language switcher (ADR-0008).
- pytest / Vitest suites with coverage gates (ADR-0009).
- pre-commit hooks, GitHub Actions CI, CD building images to GHCR, Dependabot (ADR-0010).
- `docker compose` for local PostgreSQL (ADR-0005); no database code yet.

## Capabilities

### New Capabilities
- `health-check`: liveness endpoint reporting service status and version.
- `localization`: locale negotiation (pt-BR default, en-US), localized API errors with stable codes, localized UI with language switching.
- `money`: exact monetary arithmetic rules and serialization shared by all contexts.

### Modified Capabilities

_None._

## Non-goals

- Any domain feature (auth, accounts, transactions...) — each gets its own change.
- Database access and migrations (SQLAlchemy/Alembic arrive with the first persisted context).
- Deploying to a hosting provider (pending a hosting ADR).

## References

- ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0007, ADR-0008, ADR-0009, ADR-0010, ADR-0011, ADR-0012
- RFC-0001 (accepted), RFC-0002 (context list only)

## Impact

New code only: `apps/api`, `apps/web`, `infra`, `.github/workflows`, `.pre-commit-config.yaml`, `Makefile`.
New dependencies: FastAPI, Pydantic, pytest, ruff, mypy, import-linter; React, Vite, react-i18next, Vitest, ESLint, Prettier.
