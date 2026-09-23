# ADR-0002: Backend em FastAPI + Python 3.12

- **Status:** Aceito
- **Data:** 2026-09-23
- **Relacionados:** RFC-0001

## Contexto

Precisamos de uma API HTTP com contrato OpenAPI, autenticação robusta e boa
integração futura com IA (previsão, classificação de lançamentos, agentes).

## Decisão

- **FastAPI** sobre **Python 3.12**, servido por **Uvicorn**.
- **Pydantic v2** para validação e configuração (`pydantic-settings`).
- Gerenciamento de dependências e ambientes com **uv** (`uv.lock` versionado).
- Qualidade: **ruff** (lint + format), **mypy --strict**, **import-linter** (fronteiras entre módulos).
- API versionada sob `/api/v1`; OpenAPI publicado em `/api/openapi.json`.

## Alternativas consideradas

Ver [RFC-0001](../rfc/0001-stack-options.md): NestJS, Spring Boot, Go.

## Consequências

- Duas linguagens no repositório (Python no back, TypeScript no front). Mitigação: cliente TypeScript gerado a partir do OpenAPI.
- Tipagem estática depende de disciplina (mypy strict no CI).
