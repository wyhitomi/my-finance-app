# Visão geral da arquitetura

> Diagramas detalhados (C4 e sequências) em [`diagrams.md`](diagrams.md).

```
                  ┌──────────────────────────┐
  Navegador ────► │ apps/web (React + Vite)  │  SPA estática, i18n pt-BR/en-US
                  └────────────┬─────────────┘
                               │ HTTPS  /api/v1  (JWT Bearer + cookie refresh)
                  ┌────────────▼─────────────┐
                  │ apps/api (FastAPI)       │  monólito modular
                  │ ┌────────┐ ┌──────────┐  │
                  │ │identity│ │ accounts │  │
                  │ └────────┘ └──────────┘  │
                  │ ┌────────┐ ┌──────────┐  │
                  │ │ ledger │ │budgeting │  │
                  │ └────────┘ └──────────┘  │
                  │ ┌──────────┐ ┌─────────┐ │
                  │ │reporting │ │ shared_ │ │
                  │ └──────────┘ │ kernel  │ │
                  │ ┌──────────┐ └─────────┘ │      webhooks / API
                  │ │ banking_ │◄────────────┼──── agregador Open Finance
                  │ │integrat. │             │      (ADR-0013, RFC-0004)
                  │ └──────────┘             │
                  └────────────┬─────────────┘
                               │
                  ┌────────────▼─────────────┐
                  │ PostgreSQL (schema/ctx)  │
                  └──────────────────────────┘
```

- Decisões: [`../adr`](../adr/README.md). Domínio: [RFC-0002](../rfc/0002-domain-model.md).
- Fronteiras entre módulos verificadas por `import-linter` (`apps/api/pyproject.toml`).
