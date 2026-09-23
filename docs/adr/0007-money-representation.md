# ADR-0007: Representação de dinheiro

- **Status:** Aceito
- **Data:** 2026-09-23

## Contexto

Erros de arredondamento com `float` são inaceitáveis em finanças.

## Decisão

- Valor monetário é o value object `Money(amount: Decimal, currency: Currency)` no `shared_kernel`.
- **Nunca** `float` para dinheiro — nem no Python, nem na API.
- Na API, valores trafegam como **string decimal** (`"1234.56"`) + código ISO 4217 (`"BRL"`).
- Operações entre moedas diferentes lançam erro; conversão é responsabilidade explícita (contexto `reporting`).
- Arredondamento `ROUND_HALF_EVEN` na casa decimal da moeda apenas na apresentação/fechamento; cálculos internos preservam precisão.
- No front, formatação com `Intl.NumberFormat` conforme o locale.

## Consequências

- Serialização customizada no Pydantic; testes de propriedade no `Money`.
