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
| Moeda de referência | `ReportingCurrency` | Moeda em que o usuário vê relatórios consolidados (padrão BRL). |
| Cotação | `ExchangeRate` | Taxa de conversão entre duas moedas numa data, com fonte (ex.: PTAX). |
| Detalhes de câmbio | `FxDetails` | Valor original, valor cobrado, taxa efetiva, spread e taxas (IOF, tarifas) de uma operação com câmbio. |

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
| `banking_integration` | Entrada de dados bancários externos: importação OFX/CSV (ADR-0015) e, no futuro, Open Finance (ADR-0013). Camada anticorrupção | Suporte; primeiro candidato a microsserviço |
| `exchange` | Cotações (PTAX), conversão entre moedas (ADR-0016, RFC-0006) | Suporte |
| `shared_kernel` | `Money`, `Currency` (ISO 4217), `ExchangeRate`, IDs, eventos base | Kernel compartilhado |

## Perguntas em aberto

- [x] **Moedas:** multimoeda **desde o início**, decidido em 2026-09-23 ([ADR-0016](../adr/0016-multi-currency-from-day-one.md)). Câmbio e taxas na [RFC-0006](0006-multi-currency-and-fx.md).
- [ ] **Compartilhamento:** um titular PJ pode ser acessado por mais de um usuário (ex.: sócio, contador)? Se sim, `accounts` precisa de papéis/permissões.
- [ ] **Separação PF × PJ nos relatórios:** consolidado único com filtro, ou visões separadas por padrão?
- [ ] **Recorrências** (salário, aluguel, assinaturas) ficam em `ledger` ou num contexto `scheduling` próprio?

## Fora de escopo

Importação de extratos OFX/CSV (tratada na [RFC-0005](0005-statement-file-import.md)) e investimentos com cotação. Open Finance saiu do fora de escopo e é tratado na [RFC-0004](0004-open-finance.md).
