# Backlog inicial

Cada item é uma issue (template **Feature**) e, antes de implementar, uma proposta OpenSpec (`/opsx:propose`) revisada.
Ordem sugerida = ordem de dependência.

| Issue | Título | Contexto | Depende de | Referências |
|---|---|---|---|---|
| #2 | Persistência base: SQLAlchemy async, Alembic, schemas por contexto, testes de integração com PostgreSQL | plataforma | — | ADR-0005, ADR-0004 |
| #3 | Cadastro e login com senha + JWT (access 15 min, refresh rotativo com detecção de reuso) | identity | #2 | ADR-0006, RFC-0003 |
| #4 | MFA TOTP + códigos de recuperação | identity | #3 | ADR-0006, RFC-0003 |
| #5 | Login social: Google, Microsoft, GitHub (OIDC + PKCE) | identity | #3 | ADR-0006, RFC-0003 |
| #6 | Web: telas de login/cadastro/MFA, sessão em memória, cliente da API gerado do OpenAPI | web | #3 | ADR-0003, ADR-0008 |
| #7 | Titulares PF (CPF) e PJ (CNPJ) com validação de documento | accounts | #3 | RFC-0002 |
| #8 | Contas (corrente, poupança, investimento, carteira) por titular, saldo inicial | accounts | #7 | RFC-0002, ADR-0007 |
| #9 | Cartões de crédito: limite, fechamento, vencimento, faturas e pagamento a partir de conta | accounts | #8 | RFC-0002 |
| #10 | Categorias padrão (traduzidas por chave) e personalizadas, hierárquicas | ledger | #7 | ADR-0008 |
| #11 | Lançamentos manuais: receita, despesa, transferência entre contas (inclusive PF↔PJ) | ledger | #8, #10 | ADR-0007 |
| #12 | Compras parceladas no cartão distribuídas em faturas | ledger | #9, #11 | RFC-0002 |
| #13 | Lançamentos recorrentes (salário, aluguel, assinaturas) | ledger | #11 | RFC-0002 (pergunta em aberto) |
| #14 | Orçamentos por categoria e período, com acompanhamento realizado × planejado | budgeting | #10, #11 | RFC-0002 |
| #15 | Relatório consolidado (PF, PJ e total) por período e categoria | reporting | #11 | RFC-0002 |
| #16 | Previsão de saldo (recorrências + parcelas + orçamentos) | reporting | #12, #13, #14 | RFC-0002 |
| #17 | E2E com Playwright para fluxos críticos no CI | qualidade | #6 | ADR-0009 |
| #18 | ADR de hospedagem + deploy automatizado no CD | plataforma | — | ADR-0010 |
| #19 | RFC: agente de IA do produto (assistente financeiro via tools sobre a API) | reporting | #15 | ADR-0011 |
