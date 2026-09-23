# Backlog inicial (issues a criar no GitHub)

Cada item vira uma issue (template **Feature**) e, antes de implementar, uma proposta OpenSpec (`/opsx:propose`) revisada.
Ordem sugerida = ordem de dependência.

| # | Título | Contexto | Depende de | Referências |
|---|---|---|---|---|
| 1 | Persistência base: SQLAlchemy async, Alembic, schemas por contexto, testes de integração com PostgreSQL | plataforma | — | ADR-0005, ADR-0004 |
| 2 | Cadastro e login com senha + JWT (access 15 min, refresh rotativo com detecção de reuso) | identity | 1 | ADR-0006, RFC-0003 |
| 3 | MFA TOTP + códigos de recuperação | identity | 2 | ADR-0006, RFC-0003 |
| 4 | Login social: Google, Microsoft, GitHub (OIDC + PKCE) | identity | 2 | ADR-0006, RFC-0003 |
| 5 | Web: telas de login/cadastro/MFA, sessão em memória, cliente da API gerado do OpenAPI | web | 2 | ADR-0003, ADR-0008 |
| 6 | Titulares PF (CPF) e PJ (CNPJ) com validação de documento | accounts | 2 | RFC-0002 |
| 7 | Contas (corrente, poupança, investimento, carteira) por titular, saldo inicial | accounts | 6 | RFC-0002, ADR-0007 |
| 8 | Cartões de crédito: limite, fechamento, vencimento, faturas e pagamento a partir de conta | accounts | 7 | RFC-0002 |
| 9 | Categorias padrão (traduzidas por chave) e personalizadas, hierárquicas | ledger | 6 | ADR-0008 |
| 10 | Lançamentos manuais: receita, despesa, transferência entre contas (inclusive PF↔PJ) | ledger | 7, 9 | ADR-0007 |
| 11 | Compras parceladas no cartão distribuídas em faturas | ledger | 8, 10 | RFC-0002 |
| 12 | Lançamentos recorrentes (salário, aluguel, assinaturas) | ledger | 10 | RFC-0002 (pergunta em aberto) |
| 13 | Orçamentos por categoria e período, com acompanhamento realizado × planejado | budgeting | 9, 10 | RFC-0002 |
| 14 | Relatório consolidado (PF, PJ e total) por período e categoria | reporting | 10 | RFC-0002 |
| 15 | Previsão de saldo (recorrências + parcelas + orçamentos) | reporting | 11, 12, 13 | RFC-0002 |
| 16 | E2E com Playwright para fluxos críticos no CI | qualidade | 5 | ADR-0009 |
| 17 | ADR de hospedagem + deploy automatizado no CD | plataforma | — | ADR-0010 |
| 18 | RFC: agente de IA do produto (assistente financeiro via tools sobre a API) | reporting | 14 | ADR-0011 |
