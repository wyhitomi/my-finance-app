# ADR-0005: Persistência em PostgreSQL com SQLAlchemy 2 e Alembic

- **Status:** Aceito
- **Data:** 2026-09-23
- **Relacionados:** ADR-0004

## Decisão

- **PostgreSQL 16** (dev via `docker compose`, testes de integração via Testcontainers ou serviço do CI).
- **SQLAlchemy 2.x** (async, driver `asyncpg`) com mapeamento imperativo/declarativo **somente na camada `infrastructure`** — entidades de domínio não herdam de modelos ORM.
- Migrações com **Alembic**, uma trilha única, schemas por contexto.
- Valores monetários como `NUMERIC(19,4)` + coluna de moeda (ver ADR-0007).

## Consequências

- Mapeamento domínio ↔ ORM exige código de repositório explícito (mais testável).
