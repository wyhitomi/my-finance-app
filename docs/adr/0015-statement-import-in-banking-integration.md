# ADR-0015: Importação de arquivos de extrato dentro de `banking_integration`

- **Status:** Aceito
- **Data:** 2026-09-23
- **Relacionados:** RFC-0005, ADR-0013 (amplia o escopo), ADR-0014, ADR-0004

## Contexto

O ADR-0013 criou o contexto `banking_integration` como camada anticorrupção para o
Open Finance. A importação de arquivos OFX/CSV (RFC-0005) foi priorizada, e o Open
Finance foi adiado. As duas fontes resolvem o mesmo problema: trazer dados financeiros
de fora, sem duplicar, e entregá-los ao domínio no nosso vocabulário.

## Decisão

1. O contexto `banking_integration` passa a ser o ponto único de **entrada de dados
   bancários externos**: arquivos OFX e CSV agora, e Open Finance quando for retomado.
2. As fontes ficam atrás de portas próprias da camada `application` do contexto:
   - `StatementFileParser`: um adaptador para OFX (parser próprio, ADR-0014) e outro
     para CSV.
   - `BankingProvider`: o adaptador do agregador Open Finance, quando houver.
3. A normalização (valor em `Money`, data no fuso do banco, descrição) e a
   **identidade para idempotência** (`external_id` = `FITID` ou identidade sintética)
   são compartilhadas por todas as fontes.
4. O lote de importação (`ImportBatch`: prévia, contagens, desfazer) pertence a este
   contexto. A gravação dos lançamentos e a **conciliação** continuam no `ledger`,
   chamadas pela camada `application` dele (issue #27).
5. `accounts` e `ledger` continuam sem saber de onde o dado veio: recebem apenas
   `origin = imported` e o `external_id`.
6. As regras do ADR-0004 e do import-linter valem sem mudança.

## Alternativas consideradas

| Opção | Por que não |
|---|---|
| Contexto separado `statement_import` | Duplicaria normalização e identidade de idempotência quando o Open Finance voltar, ou criaria dependência entre os dois contextos. |

## Consequências

- O contexto nasce com a importação de arquivos (issues #25, #26 e #28), antes do
  Open Finance.
- Se um dia `banking_integration` for extraído como microsserviço (ADR-0004), a
  importação de arquivos vai junto.
