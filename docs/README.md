# Documentação

| Pasta | Conteúdo |
|---|---|
| [`adr/`](adr/README.md) | **Architecture Decision Records** — decisões tomadas, imutáveis após aceitas (substituídas por novos ADRs). |
| [`rfc/`](rfc/README.md) | **Requests for Comments** — propostas abertas à discussão, antes de virarem decisão (ADR) ou mudança (OpenSpec). |
| [`architecture/`](architecture/overview.md) | Visão geral da arquitetura e [diagramas](architecture/diagrams.md) (contexto, containers, bounded contexts, fluxos de login e Open Finance). |
| [`releases.md`](releases.md) | Como as versões e releases são geradas (release-please) e configuração do token. |
| [`guides/`](guides/) | **Guias de uso:** [ADRs e RFCs](guides/adr-and-rfc.md) e [OpenSpec](guides/openspec.md). |
| [`../openspec/`](../openspec) | Especificações vivas (`specs/`) e propostas de mudança (`changes/`). |

## Fluxo de trabalho

```
Ideia ──► RFC (se houver dúvida de arquitetura/produto)
            │ aceita
            ▼
          ADR (registra a decisão)
            │
            ▼
   OpenSpec change (proposal → specs → design → tasks)
            │ tasks começam pelos testes (TDD)
            ▼
   Implementação ──► CI verde ──► openspec archive
```

Regras inegociáveis (valem para pessoas e agentes de IA):

1. **Nunca implementar sem ler os ADRs e RFCs relevantes.** Toda proposta OpenSpec cita os ADRs/RFCs em que se apoia.
2. **Nunca implementar sem testes.** O teste que falha vem antes do código de produção.
3. Contradizer um ADR aceito exige um novo ADR que o substitua — nunca um desvio silencioso.
