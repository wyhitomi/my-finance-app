# ADR-0016: Múltiplas moedas desde a primeira versão

- **Status:** Aceito
- **Data:** 2026-09-23
- **Relacionados:** RFC-0006, RFC-0002, ADR-0007, ADR-0004

## Contexto

A RFC-0002 perguntava se o produto começaria só com BRL. O dono do produto decidiu que
o suporte a múltiplas moedas deve existir desde o início. Adiar a decisão obrigaria a
migrar dados e regras de moeda única para multimoeda depois, o que é caro e arriscado.

## Decisão

1. Contas, cartões e lançamentos aceitam **qualquer moeda ISO 4217**. Cada conta e cada
   cartão têm uma moeda fixa.
2. O `Money` do `shared_kernel` passa a usar a tabela ISO 4217 completa, com as **casas
   decimais corretas de cada moeda**. A mudança segue o fluxo OpenSpec, alterando a spec
   `money`.
3. Cada usuário escolhe uma **moeda de referência** para relatórios, com BRL como padrão.
4. Valores em moedas diferentes **nunca** são somados sem conversão explícita (reforça o
   ADR-0007). Toda conversão registra a cotação usada, a fonte e a data.
5. Lançamentos que envolvem câmbio guardam o **valor original**, o **valor cobrado** e as
   **taxas** (IOF, tarifas). O spread é calculado contra uma cotação de referência
   (modelo `FxDetails` da RFC-0006).
6. Cotações e conversão ficam num contexto novo, `exchange`, atrás de uma porta
   `RateProvider`. A escolha da fonte (PTAX recomendada) terá ADR próprio após a
   validação técnica.

## Alternativas consideradas

| Opção | Por que não |
|---|---|
| Só BRL no início | Descartada pelo dono do produto. |
| Moeda única por usuário, com conversão na entrada | Perde o valor original e distorce saldos e custos de câmbio. |

## Consequências

- Os modelos de `accounts` (#8, #9) e `ledger` (#11) nascem com moeda por conta e com
  campos de câmbio.
- Relatórios (#15) e previsão (#16) precisam de conversão e de sinalização de valores
  convertidos.
- Surge uma dependência de uma fonte externa de cotações, com busca diária e
  armazenamento local.
