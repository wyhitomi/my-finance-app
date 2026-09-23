# ADR-0004: Monólito modular orientado a DDD, com caminho para microsserviços

- **Status:** Aceito
- **Data:** 2026-09-23
- **Relacionados:** RFC-0001, RFC-0002

## Contexto

Os requisitos pedem monólito modular **e** microsserviços. Para um produto
pessoal, microsserviços desde o dia 1 trazem custo operacional (rede, deploy,
consistência distribuída) sem benefício. Mas queremos poder extrair partes
(ex.: `reporting`/previsão, agentes de IA) sem reescrever.

## Decisão

1. O backend é **um deploy** com módulos por **bounded context**:
   `identity`, `accounts`, `ledger`, `budgeting`, `reporting`, mais `shared_kernel`.
2. Cada módulo segue camadas hexagonais:
   ```
   modules/<ctx>/
     domain/          # entidades, value objects, eventos — Python puro, sem framework
     application/     # casos de uso, portas (interfaces), DTOs — API pública do módulo
     infrastructure/  # adaptadores: SQLAlchemy, OAuth, e-mail...
     api/             # routers FastAPI
   ```
3. **Regras de dependência** (verificadas por `import-linter` no CI):
   - `domain` não importa `application`, `infrastructure`, `api`, FastAPI nem SQLAlchemy.
   - Um módulo **não importa** o interior de outro. Comunicação entre contextos apenas via `application` do outro módulo ou **eventos de domínio**.
   - Todos podem importar `shared_kernel`.
4. Cada contexto tem seu próprio schema no PostgreSQL (ex.: `identity.users`); **sem foreign keys entre schemas** — referências por ID.
5. Critério para extrair microsserviço (exige novo ADR): necessidade real de escala independente, linguagem/runtime diferente ou ciclo de deploy próprio.

## Consequências

- Extração futura = trocar chamadas in-process por HTTP/mensageria no adaptador; domínio intacto.
- Um pouco mais de cerimônia (portas/adaptadores) do que um CRUD simples.
