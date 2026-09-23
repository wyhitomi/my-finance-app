# ADR-0010: CI/CD com GitHub Actions e pre-commit hooks

- **Status:** Aceito
- **Data:** 2026-09-23

## Decisão

- **pre-commit** (framework `pre-commit`) roda localmente: ruff, ruff-format, mypy, ESLint, Prettier, checagens de YAML/JSON, detecção de segredos (**gitleaks**), mensagens **Conventional Commits** (`commit-msg`).
- **CI** (`.github/workflows/ci.yml`) em todo PR e push na `main`, jobs paralelos:
  - `api`: ruff, mypy, import-linter, pytest com cobertura.
  - `web`: ESLint, typecheck, Vitest com cobertura, build.
  - `specs`: `openspec validate --all --strict`.
  - `pre-commit`: roda todos os hooks sobre o repositório (garante que ninguém pulou com `--no-verify`).
- **CD** (`.github/workflows/cd.yml`): na `main`, constrói imagens Docker da API e do web e publica no **GHCR**. Deploy para um ambiente de hospedagem fica pendente da escolha do provedor (novo ADR).
- Dependabot para Actions, pip (uv) e npm.

## Consequências

- Branch protection na `main` exigindo CI verde deve ser configurada manualmente no GitHub.
