# ADR-0009: Estratégia de testes e TDD

- **Status:** Aceito
- **Data:** 2026-09-23

## Decisão

- **TDD obrigatório:** o teste que falha é escrito antes do código de produção (red → green → refactor). Tarefas OpenSpec são ordenadas test-first.
- Pirâmide:

  | Camada | Ferramenta | Alvo |
  |---|---|---|
  | Domínio (unit) | pytest | Entidades, value objects, regras — rápidos, sem I/O |
  | Aplicação | pytest + fakes das portas | Casos de uso |
  | Integração | pytest + httpx `AsyncClient` + PostgreSQL real | API e repositórios |
  | Arquitetura | import-linter | Fronteiras de módulos |
  | Front (componentes) | Vitest + Testing Library | Telas e hooks |
  | E2E | Playwright | Fluxos críticos (login, lançamento, orçamento) |

- Cobertura mínima: **90% no backend** (`domain` + `application`), **80% no front**; o CI falha abaixo disso.
- Cenários GIVEN/WHEN/THEN das specs OpenSpec mapeiam 1:1 para testes.

## Consequências

- Ritmo inicial mais lento, regressões raras; agentes de IA têm um oráculo objetivo para validar o próprio trabalho.
