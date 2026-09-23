# RFC-0004: Contas manuais e contas conectadas via Open Finance

- **Status:** Adiada. Sem orçamento para agregador por enquanto (decisão de 2026-09-23). A importação de arquivos OFX/CSV ([RFC-0005](0005-statement-file-import.md)) vem antes. O modelo de origem do ADR-0013 continua valendo.
- **Autor(es):** Hitomi Growth + Claude Code
- **Criada em:** 2026-09-23
- **ADRs resultantes:** [ADR-0013](../adr/0013-account-sources-and-banking-integration.md) (modelo de origem e contexto de integração). A escolha do agregador ficará num ADR futuro.

## Resumo

Toda conta e todo cartão passam a ter uma **origem**: `manual`, com lançamentos
digitados pelo usuário, ou `open_finance`, com saldo e transações importados de uma
instituição via Open Finance Brasil. As duas convivem para o mesmo titular (PF ou PJ).
A integração fica num bounded context novo, `banking_integration`, que funciona como
**camada anticorrupção**: traduz o modelo do provedor para o nosso domínio, e nenhum
outro contexto conhece o provedor.

## Motivação

Digitar tudo à mão dá controle, mas cansa e gera esquecimentos. Open Finance traz
saldo e extrato automaticamente, inclusive de contas e cartões PJ. Contas sem Open
Finance (dinheiro, bancos não participantes, investimentos específicos) continuam
manuais.

## Como o acesso aos dados funciona

No Open Finance Brasil, só **instituições autorizadas pelo Banco Central** recebem dados
diretamente. Um app pessoal não se torna receptor. O caminho viável é um **agregador**
autorizado, que conduz o consentimento do usuário no banco e expõe uma API e webhooks
para o nosso backend.

```
Usuário ──► widget/redirect do agregador ──► banco (consentimento Open Finance)
                                                   │
Nosso backend ◄── API + webhooks do agregador ◄────┘
   banking_integration (ACL) ──eventos──► accounts / ledger
```

- **Não armazenamos credenciais bancárias.** Guardamos apenas os identificadores de
  conexão e consentimento do agregador.
- O consentimento **expira** e precisa ser renovado pelo usuário. Hoje o prazo máximo é
  de 12 meses, e o app deve avisar antes do vencimento.

## Proposta detalhada

### Modelo de domínio

| Conceito | Mudança |
|---|---|
| `Account.source` / `CreditCard.source` | `manual` \| `open_finance`. Uma conta conectada guarda o `connection_id` e o identificador externo. |
| `Transaction.origin` | `manual` \| `imported` \| `recurring`. Lançamento importado guarda `external_id`, que é único por conta e garante importação idempotente. |
| `BankConnection` (novo, `banking_integration`) | Instituição, titular, status (`active`, `syncing`, `expired`, `error`, `revoked`), validade do consentimento, última sincronização. |

### Regras de negócio

1. **Lançamentos importados:** valor, data e conta vêm da instituição e são somente
   leitura. Categoria, descrição personalizada, tags e divisão podem ser editadas.
   Excluir um importado significa **ocultar**, para que ele não volte na próxima
   sincronização.
2. **Saldo de conta conectada:** o saldo informado pela instituição é a referência.
   Se a soma dos lançamentos divergir, o app mostra um alerta. Ele não "corrige"
   silenciosamente.
3. **Lançamentos manuais em conta conectada** são permitidos (ex.: registrar antes de
   compensar). Na importação, o app busca **correspondências**: mesma conta, mesmo
   valor, data em ±3 dias e descrição parecida. A correspondência é sugerida e o
   usuário confirma a conciliação. Nada é mesclado sem confirmação.
4. **Converter uma conta manual em conectada** preserva o histórico. A importação só
   traz o período que ainda não existe e roda a conciliação da regra 3 na sobreposição.
5. **Desconectar** mantém o histórico já importado, e a conta vira `manual`. O usuário
   também pode pedir a **exclusão dos dados importados** (LGPD).
6. **Cartões conectados:** faturas, limite e parcelas vêm da instituição. Parcelas
   importadas não são recalculadas por nós.
7. **Categorização:** o app sugere a categoria a partir da categoria do provedor e do
   histórico do usuário. Esse é o primeiro caso de uso candidato para IA (issue #19).

### Sincronização

- Feita por **webhook** do agregador (assinatura verificada), com um job periódico
  como rede de segurança.
- Idempotente pelo `external_id`. Reprocessar nunca duplica.
- Cada tipo de falha vira um status visível: consentimento expirado, instituição fora
  do ar ou erro de dados.

### Por que um contexto separado

`banking_integration` tem ciclo de vida próprio (webhooks, filas, retentativas,
segredos do provedor) e é o **candidato mais forte a microsserviço** (ADR-0004). Os
contextos `accounts` e `ledger` recebem comandos e eventos no **nosso** vocabulário:
trocar de agregador afeta só esse contexto.

## Alternativas

| Opção | Por que não |
|---|---|
| Tornar-se participante direto do Open Finance | Exige autorização do Banco Central como instituição. Inviável para um app pessoal. |
| Importar extratos OFX/CSV | Continua útil como **complemento** para bancos sem Open Finance. Tratado na [RFC-0005](0005-statement-file-import.md), reaproveitando a mesma conciliação. |
| Raspagem de internet banking (screen scraping) | Insegura, frágil e contrária aos termos dos bancos. Descartada. |

## Perguntas em aberto

- [ ] **Qual agregador?** Candidatos: **Pluggy** e **Belvo**, entre outros. Critérios:
      cobertura de bancos PF e PJ, suporte a cartão de crédito, preço para poucas
      conexões, sandbox, qualidade dos webhooks e SDK do widget. Preços e planos
      precisam ser conferidos com os fornecedores antes da decisão.
- [ ] **Orçamento mensal** aceitável para o agregador. O custo costuma ser por conexão
      ativa.
- [ ] **Histórico inicial:** quantos meses importar na primeira conexão (ex.: 12)?
- [ ] **Conciliação automática:** algum caso pode conciliar sem confirmação (ex.:
      correspondência exata de valor, data e descrição)?

## Fora de escopo

Iniciação de pagamentos (Pix via Open Finance), investimentos com cotação,
portabilidade de crédito.
