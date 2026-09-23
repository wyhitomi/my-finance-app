# ADR-0001: Registrar decisões de arquitetura

- **Status:** Aceito
- **Data:** 2026-09-23

## Contexto

O projeto será desenvolvido por uma pessoa com apoio intenso de agentes de IA.
Agentes não têm memória entre sessões: sem registro escrito, decisões são
reabertas ou violadas sem perceber.

## Decisão

Vamos registrar toda decisão arquitetural significativa como ADR em `docs/adr/`,
no formato de [`template.md`](template.md), numeração sequencial de 4 dígitos.
Propostas ainda em debate vão para `docs/rfc/`. ADRs aceitos são imutáveis: para
mudar uma decisão, cria-se um novo ADR que substitui o anterior.

## Consequências

- Agentes (via `AGENTS.md` e `openspec/config.yaml`) são instruídos a ler ADRs/RFCs antes de propor ou implementar.
- Custo pequeno de escrita a cada decisão.
