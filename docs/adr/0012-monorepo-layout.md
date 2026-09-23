# ADR-0012: Monorepo

- **Status:** Aceito
- **Data:** 2026-09-23

## Decisão

Um único repositório:

```
apps/api/        # FastAPI (uv)
apps/web/        # React + Vite (pnpm)
docs/            # ADRs, RFCs, arquitetura
openspec/        # specs e mudanças
infra/           # docker compose, IaC futura
.github/         # CI/CD, templates, instruções de agentes
```

Tarefas comuns via `Makefile` na raiz (`make setup`, `make check`, `make test`).

## Consequências

- Uma mudança que atravessa API e front vai em um único PR, com CI por caminho.
