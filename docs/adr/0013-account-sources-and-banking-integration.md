# ADR-0013: Origem das contas (manual e Open Finance) e contexto `banking_integration`

- **Status:** Aceito
- **Data:** 2026-09-23
- **Relacionados:** RFC-0004, RFC-0002, ADR-0004, ADR-0007

## Contexto

O produto precisa suportar contas digitadas à mão e contas conectadas via Open Finance
Brasil, para titulares PF e PJ. Acesso direto ao Open Finance exige autorização do
Banco Central, então os dados virão de um agregador autorizado (a escolher, ADR futuro).
Este ADR complementa o ADR-0004: acrescenta um contexto e não altera os existentes.

## Decisão

1. Contas e cartões têm `source: manual | open_finance`. Lançamentos têm
   `origin: manual | imported | recurring`, e os importados carregam `external_id`
   único por conta.
2. Criamos o bounded context **`banking_integration`**, uma camada anticorrupção que
   concentra conexões, consentimentos, webhooks e sincronização. Só ele conhece o
   agregador, atrás de uma porta (`BankingProvider`) com um adaptador por fornecedor.
3. `banking_integration` conversa com `accounts` e `ledger` apenas pela camada
   `application` deles ou por eventos de domínio, como os demais contextos. As mesmas
   regras do import-linter valem para ele.
4. Importação idempotente pelo `external_id`. Conciliação com lançamentos manuais é
   **sugerida** e confirmada pelo usuário.
5. Não armazenamos credenciais bancárias. Segredos do agregador ficam em variáveis de
   ambiente/secrets. Webhooks exigem verificação de assinatura.
6. `banking_integration` é o primeiro candidato a extração como microsserviço. A
   extração só acontece com novo ADR, conforme os critérios do ADR-0004.

## Alternativas consideradas

| Opção | Por que não |
|---|---|
| Integração do agregador dentro de `accounts`/`ledger` | Acopla o domínio ao modelo do fornecedor. Trocar de agregador exigiria mexer no core. |
| Tratar contas conectadas como um tipo separado de conta | Duplica regras (saldo, faturas, orçamentos, relatórios). A origem é um atributo, não outro conceito. |

## Consequências

- Orçamentos, relatórios e previsão funcionam igual para as duas origens.
- A conciliação passa a ser uma regra de negócio relevante no `ledger`.
- Surgem dependências operacionais novas (webhooks públicos, jobs de sincronização),
  que pesam no ADR de hospedagem (issue #18).
