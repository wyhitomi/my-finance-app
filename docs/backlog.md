# Backlog inicial

Cada item é uma issue (template **Feature**) e, antes de implementar, uma proposta OpenSpec (`/opsx:propose`) revisada.
Ordem sugerida = ordem de dependência. Decisão de 2026-09-23: **importação de arquivos OFX/CSV antes do Open Finance**. Open Finance fica adiado (label `adiado`) enquanto não houver orçamento para agregador.

| Issue | Título | Contexto | Depende de | Referências |
|---|---|---|---|---|
| #2 | Persistência base: SQLAlchemy async, Alembic, schemas por contexto, testes de integração com PostgreSQL | plataforma | — | ADR-0005, ADR-0004 |
| #3 | Cadastro e login com senha + JWT (access 15 min, refresh rotativo com detecção de reuso) | identity | #2 | ADR-0006, RFC-0003 |
| #4 | MFA TOTP + códigos de recuperação | identity | #3 | ADR-0006, RFC-0003 |
| #5 | Login social: Google, Microsoft, GitHub (OIDC + PKCE) | identity | #3 | ADR-0006, RFC-0003 |
| #6 | Web: telas de login/cadastro/MFA, sessão em memória, cliente da API gerado do OpenAPI | web | #3 | ADR-0003, ADR-0008 |
| #7 | Titulares PF (CPF) e PJ (CNPJ) com validação de documento | accounts | #3 | RFC-0002 |
| #8 | Contas (corrente, poupança, investimento, carteira) por titular, saldo inicial, origem manual/Open Finance | accounts | #7 | RFC-0002, ADR-0007 |
| #9 | Cartões de crédito: limite, fechamento, vencimento, faturas e pagamento a partir de conta, origem manual/Open Finance | accounts | #8 | RFC-0002 |
| #10 | Categorias padrão (traduzidas por chave) e personalizadas, hierárquicas | ledger | #7 | ADR-0008 |
| #11 | Lançamentos manuais: receita, despesa, transferência entre contas (inclusive PF↔PJ), campo de origem | ledger | #8, #10 | ADR-0007 |
| #12 | Compras parceladas no cartão distribuídas em faturas | ledger | #9, #11 | RFC-0002 |
| #13 | Lançamentos recorrentes (salário, aluguel, assinaturas) | ledger | #11 | RFC-0002 (pergunta em aberto) |
| #14 | Orçamentos por categoria e período, com acompanhamento realizado × planejado | budgeting | #10, #11 | RFC-0002 |
| #15 | Relatório consolidado (PF, PJ e total) por período e categoria | reporting | #11 | RFC-0002 |
| #16 | Previsão de saldo (recorrências + parcelas + orçamentos) | reporting | #12, #13, #14 | RFC-0002 |
| #17 | E2E com Playwright para fluxos críticos no CI | qualidade | #6 | ADR-0009 |
| #18 | ADR de hospedagem + deploy automatizado no CD | plataforma | — | ADR-0010 |
| #19 | RFC: agente de IA do produto (assistente financeiro via tools sobre a API) | reporting | #15 | ADR-0011 |
| #20 ⏸ | Escolher agregador Open Finance (Pluggy, Belvo...) e registrar ADR | banking_integration | — | RFC-0004 |
| #21 ⏸ | Conectar instituição: widget do agregador, consentimento, `BankConnection`, webhooks assinados | banking_integration | #20, #8 | ADR-0013, RFC-0004 |
| #22 ⏸ | Sincronizar contas e cartões conectados (saldo, limite, faturas, parcelas) | banking_integration | #21, #9 | ADR-0013, RFC-0004 |
| #23 ⏸ | Importar transações via Open Finance (idempotente por `external_id`) | banking_integration | #22, #11, #27 | ADR-0013, RFC-0004 |
| #24 ⏸ | Consentimento: aviso de expiração, renovação, desconexão e exclusão de dados (LGPD) | banking_integration | #21 | RFC-0004 |
| #25 | Parser OFX 1.x (SGML) e 2.x (XML), parser próprio MIT | banking_integration | #11 | RFC-0005 |
| #26 | Upload de extrato: prévia, deduplicação, lote e desfazer | banking_integration | #25, #11 | RFC-0005 |
| #27 | Conciliação de lançamentos importados com manuais | ledger | #11 | RFC-0004, RFC-0005 |
| #28 | CSV com assistente de mapeamento de colunas e modelos por conta | banking_integration | #26 | RFC-0005 |

⏸ = adiado.
