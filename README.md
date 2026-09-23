# My Finance App

Gestor financeiro pessoal para quem tem vida financeira **PF e PJ**: múltiplas contas
(manuais ou conectadas via **Open Finance**), cartões de crédito, lançamentos manuais e importados, orçamentos e relatórios (consolidado e previsão),
com login seguro (senha, Google/Microsoft/GitHub, MFA) em **pt-BR** e **en-US**.

> Status: scaffold. As features estão planejadas como issues e serão especificadas via OpenSpec.

## Stack

| Camada | Tecnologia | Decisão |
|---|---|---|
| Backend | FastAPI · Python 3.12 · uv · monólito modular DDD | [ADR-0002](docs/adr/0002-backend-fastapi.md), [ADR-0004](docs/adr/0004-modular-monolith-ddd.md) |
| Frontend | React 19 · Vite · TypeScript · react-i18next | [ADR-0003](docs/adr/0003-frontend-react-vite.md) |
| Dados | PostgreSQL 16 · SQLAlchemy 2 · Alembic | [ADR-0005](docs/adr/0005-persistence-postgresql.md) |
| Auth | JWT · Argon2id · OAuth2/OIDC · TOTP | [ADR-0006](docs/adr/0006-authentication.md) |
| Qualidade | TDD · pytest · Vitest · import-linter · pre-commit | [ADR-0009](docs/adr/0009-testing-strategy-tdd.md), [ADR-0010](docs/adr/0010-ci-cd-and-pre-commit.md) |
| Releases | release-please · SemVer · CHANGELOG por app | [ADR-0017](docs/adr/0017-release-management-with-release-please.md) |
| IA | OpenSpec · AGENTS.md | [ADR-0011](docs/adr/0011-spec-driven-development-and-ai-agents.md) |

## Começando

Pré-requisitos: Python via [uv](https://docs.astral.sh/uv/), Node 22 + pnpm, Docker.

```bash
make setup      # dependências + git hooks
make check      # tudo que o CI roda
make db-up      # PostgreSQL local
make api-dev    # http://localhost:8000/api/docs
make web-dev    # http://localhost:5173
```

## Como contribuir (pessoas e agentes de IA)

1. Leia [`AGENTS.md`](AGENTS.md), os [ADRs](docs/adr/README.md) e as [RFCs](docs/rfc/README.md).
   Guias: [como usar ADRs e RFCs](docs/guides/adr-and-rfc.md) e [como usar o OpenSpec](docs/guides/openspec.md).
2. Proponha a mudança com OpenSpec (`/opsx:propose`), revise, depois implemente (`/opsx:apply`) **com testes primeiro**.
3. `make check` verde, PR com o template preenchido, e `/opsx:archive` ao concluir.
