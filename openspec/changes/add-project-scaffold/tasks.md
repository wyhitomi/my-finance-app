# Tasks

## 1. Tooling
- [ ] 1.1 Create `apps/api` uv project with ruff, mypy (strict), pytest, coverage and import-linter config
- [ ] 1.2 Create `apps/web` Vite + React + TS project with ESLint, Prettier, Vitest
- [ ] 1.3 Add root `Makefile`, `.pre-commit-config.yaml`, `.editorconfig`, `.gitignore`, `infra/docker-compose.yml`

## 2. Money (shared kernel)
- [ ] 2.1 Write failing unit tests for every `money` spec scenario
- [ ] 2.2 Implement `Currency` and `Money` until tests pass

## 3. API platform
- [ ] 3.1 Write failing integration tests for health and OpenAPI scenarios
- [ ] 3.2 Implement app factory, settings and health router
- [ ] 3.3 Write failing unit tests for `negotiate_locale` and catalog key parity
- [ ] 3.4 Implement locale negotiation and catalogs
- [ ] 3.5 Write failing integration tests for `Content-Language` and the localized 404 envelope
- [ ] 3.6 Implement locale middleware and error handlers
- [ ] 3.7 Create bounded-context packages and import-linter contracts; `lint-imports` passes

## 4. Web
- [ ] 4.1 Write failing tests: pt-BR default, switch to en-US updates text and `lang`, catalog key parity
- [ ] 4.2 Implement i18n setup, App shell and LanguageSwitcher

## 5. Delivery
- [ ] 5.1 Add CI workflow (api, web, specs, pre-commit jobs)
- [ ] 5.2 Add CD workflow building API and web images to GHCR; Dockerfiles
- [ ] 5.3 Add Dependabot, PR template, issue templates
- [ ] 5.4 Run `make check` green and archive this change
