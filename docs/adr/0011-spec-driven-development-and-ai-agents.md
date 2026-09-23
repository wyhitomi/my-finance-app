# ADR-0011: Desenvolvimento guiado por especificação (OpenSpec) e suporte a agentes de IA

- **Status:** Aceito
- **Data:** 2026-09-23
- **Relacionados:** ADR-0001, ADR-0009

## Contexto

Boa parte do código será escrita com agentes de IA (Claude Code, GitHub Copilot
e outros). Agentes produzem melhor quando há especificação explícita e regras
legíveis por máquina.

## Decisão

- **OpenSpec** (`openspec/`) é a fonte de verdade do comportamento:
  - `openspec/specs/` — specs vivas por capability.
  - `openspec/changes/` — propostas (proposal, design, specs delta, tasks); arquivadas após implementadas.
- Toda feature começa com `/opsx:propose` e só é implementada com `/opsx:apply` após revisão humana da proposta.
- **`AGENTS.md`** na raiz é o manual para qualquer agente (padrão aberto); `CLAUDE.md` e `.github/copilot-instructions.md` apontam para ele.
- Skills/commands do OpenSpec instalados para Claude Code (`.claude/`), Copilot (`.github/`) e genéricos (`.agents/`).
- A API expõe OpenAPI completo, que serve de contrato também para futuros **agentes de IA do produto** (ex.: um assistente financeiro que consulta relatórios via tools). Esse agente de produto será tema de RFC própria.

## Consequências

- Mudanças sem proposta OpenSpec são rejeitadas em revisão (exceto correções triviais e chores).
