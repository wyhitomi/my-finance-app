# Design

## Context

First code in the repository. Implements the foundation described by ADR-0002…0012
without domain features. Bounded contexts touched: `shared_kernel` (Money) and
cross-cutting `core` (config, i18n). Context packages are created empty.

## Decisions

### Backend layout
```
apps/api/
  pyproject.toml          # uv project, ruff/mypy/pytest/import-linter config
  src/finance_api/
    main.py               # create_app(settings) factory
    core/config.py        # pydantic-settings (FINANCE_ prefix)
    core/i18n/            # locale negotiation, message catalogs, middleware
    core/errors.py        # AppError + localized error envelope handlers
    api/v1/health.py      # platform router
    shared_kernel/money.py
    modules/{identity,accounts,ledger,budgeting,reporting}/{domain,application,infrastructure,api}
  tests/{unit,integration,architecture}
```
- Locale is resolved by a pure function (`negotiate_locale`) and stored in a
  `ContextVar` by a middleware, so domain/application code can translate without
  depending on FastAPI.
- Message catalogs are Python dicts keyed by stable codes (`common.not_found`); a
  unit test asserts both locales have identical keys. gettext was considered but
  is heavier than needed for API-only messages.
- `Money` is a frozen dataclass wrapping `Decimal`; the constructor rejects `float`
  and unknown currencies. Only a small ISO 4217 subset (BRL, USD, EUR) is enabled
  until RFC-0002's multi-currency question is answered.
- Architecture contracts (import-linter): domain layers are framework-free;
  modules are independent of each other; everything may use `shared_kernel`.

### Frontend layout
```
apps/web/src/
  app/App.tsx             # shell
  i18n/index.ts           # i18next init, supported locales, detection
  i18n/locales/{pt-BR,en-US}/common.json
  shared/components/LanguageSwitcher.tsx
```
- Language detection: `localStorage` → `navigator.language` → `pt-BR`.
- `document.documentElement.lang` updated on language change.

## Test strategy

- Unit (pytest): `Money`, `negotiate_locale`, catalog completeness.
- Integration (pytest + httpx ASGI transport): health, OpenAPI, locale header, 404 envelope.
- Architecture: `lint-imports` in `make check` and CI.
- Web (Vitest + Testing Library): App renders pt-BR by default, switching to en-US, catalog key parity.

## Risks / Trade-offs

- Empty module packages may look like ceremony; they make boundaries visible and
  let import-linter guard them from the first feature.
