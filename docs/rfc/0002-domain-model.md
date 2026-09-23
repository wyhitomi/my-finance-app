# RFC-0002: Modelo de domínio e bounded contexts

- **Status:** Em discussão
- **Autor(es):** Hitomi Growth + Claude Code
- **Criada em:** 2026-09-23
- **ADRs resultantes:** [ADR-0004](../adr/0004-modular-monolith-ddd.md) (estrutura dos módulos)

## Resumo

Define a linguagem ubíqua e os bounded contexts do produto. A estrutura de
pastas dos módulos já existe no scaffold; o conteúdo de cada contexto será
detalhado nas propostas OpenSpec correspondentes.

## Linguagem ubíqua

| Termo (pt-BR) | Termo (código) | Definição |
|---|---|---|
| Usuário | `User` | Pessoa que faz login. Dona de um ou mais titulares. |
| Titular | `Holder` | Entidade financeira: **PF** (CPF) ou **PJ** (CNPJ). Um usuário pode ter vários (ex.: ele mesmo + sua empresa). |
| Conta | `Account` | Conta corrente, poupança, investimento ou carteira (dinheiro) pertencente a um titular. Origem **manual** ou **Open Finance** (RFC-0004). |
| Cartão de crédito | `CreditCard` | Instrumento com limite, dia de fechamento e dia de vencimento; gera faturas. Origem manual ou Open Finance. |
| Fatura | `Statement` | Período de um cartão; paga a partir de uma conta. |
| Lançamento | `Transaction` | Receita, despesa ou transferência, com data, valor (`Money`), categoria. Origem manual, importada ou recorrente. |
| Conexão bancária | `BankConnection` | Vínculo com uma instituição via Open Finance: consentimento, validade, status de sincronização. |
| Conciliação | `Reconciliation` | Associação confirmada entre um lançamento manual e um importado que representam o mesmo fato. |
| Parcelamento | `Installment` | Despesa no cartão dividida em N faturas. |
| Categoria | `Category` | Classificação hierárquica de lançamentos. |
| Orçamento | `Budget` | Limite planejado por categoria e período. |
| Previsão | `Forecast` | Projeção de saldo com base em recorrências, parcelas e orçamentos. |

## Bounded contexts

```
┌───────────┐     UserId      ┌───────────┐  AccountId/CardId  ┌───────────┐
│ identity  │ ──────────────► │ accounts  │ ─────────────────► │  ledger   │
│ (auth,MFA)│                 │ (PF/PJ,   │                    │(lançamen- │
└───────────┘                 │ contas,   │                    │ tos,cate- │
                              │ cartões)  │                    │ gorias)   │
                              └───────────┘                    └─────┬─────┘
                                                                     │ eventos
                                              ┌──────────────────────┼─────────┐
                                              ▼                      ▼         │
                                        ┌───────────┐          ┌───────────┐   │
                                        │ budgeting │ ───────► │ reporting │ ◄─┘
                                        └───────────┘          │(consolid.,│
                                                               │ previsão) │
                                                               └───────────┘

┌─────────────────────┐  comandos/eventos (nosso vocabulário)
│ banking_integration │ ────────────────► accounts, ledger
│ (Open Finance, ACL) │ ◄──── webhooks do agregador
└─────────────────────┘
```

| Contexto | Responsabilidade | Tipo |
|---|---|---|
| `identity` | Cadastro, senha, login social, MFA, sessões/tokens | Genérico (suporte) |
| `accounts` | Titulares PF/PJ, contas, cartões, faturas | Core |
| `ledger` | Lançamentos, transferências, parcelas, categorias | Core |
| `budgeting` | Orçamentos e acompanhamento | Core |
| `reporting` | Relatórios consolidados e previsão (read models) | Core; candidato a microsserviço |
| `banking_integration` | Conexões Open Finance via agregador, sincronização, webhooks (camada anticorrupção, ADR-0013) | Suporte; primeiro candidato a microsserviço |
| `shared_kernel` | `Money`, `Currency`, IDs, eventos base | Kernel compartilhado |

## Perguntas em aberto

- [ ] **Moedas:** só BRL no início, ou multimoeda (ex.: conta em USD) desde já? Afeta relatórios consolidados (conversão de câmbio).
- [ ] **Compartilhamento:** um titular PJ pode ser acessado por mais de um usuário (ex.: sócio, contador)? Se sim, `accounts` precisa de papéis/permissões.
- [ ] **Separação PF × PJ nos relatórios:** consolidado único com filtro, ou visões separadas por padrão?
- [ ] **Recorrências** (salário, aluguel, assinaturas) ficam em `ledger` ou num contexto `scheduling` próprio?

## Fora de escopo

Importação de extratos OFX/CSV (feature futura, reaproveita a conciliação da RFC-0004) e investimentos com cotação. Open Finance saiu do fora de escopo e é tratado na [RFC-0004](0004-open-finance.md).
