# AGENTS.md

Instruções para qualquer agente de IA (Claude Code, GitHub Copilot, Codex, Cursor...) e para pessoas.

## Produto

Gestor financeiro pessoal: múltiplas contas PF/PJ (manuais ou via Open Finance), cartões de crédito,
lançamentos manuais e importados, orçamentos, relatórios (consolidado e previsão), i18n pt-BR/en-US, login
seguro (senha, social, MFA). Detalhes: `openspec/config.yaml` e `docs/`.

Guias: [ADRs e RFCs](docs/guides/adr-and-rfc.md) · [OpenSpec](docs/guides/openspec.md).

## Regras obrigatórias

1. **Leia `docs/adr/` e `docs/rfc/` antes de propor ou implementar.** Cite os ADRs/RFCs usados.
2. **Nunca implemente sem teste.** Escreva o teste que falha, veja-o falhar, depois implemente (ADR-0009).
3. **Features começam no OpenSpec:** `/opsx:propose` → revisão humana → `/opsx:apply` → `/opsx:archive`.
   Não pule a revisão humana da proposta.
4. Contradizer um ADR aceito exige um novo ADR que o substitua. Pergunte ao humano se houver dúvida.
5. Respeite as fronteiras dos módulos (ADR-0004); `make check` roda o import-linter.
6. Dinheiro é `Money`/`Decimal`, nunca `float` (ADR-0007).
7. Todo texto visível ao usuário usa chaves de tradução em pt-BR **e** en-US (ADR-0008).
8. Commits no padrão Conventional Commits. Não use `--no-verify`. O tipo define a versão e o CHANGELOG via
   release-please (ADR-0017): nunca edite versões nem `CHANGELOG.md` à mão.

## Estrutura

```
apps/api/src/finance_api/
  main.py                 # app factory FastAPI
  core/                   # config, i18n, infraestrutura transversal
  shared_kernel/          # Money, Currency, IDs, eventos
  modules/<contexto>/{domain,application,infrastructure,api}
apps/api/tests/{unit,integration,architecture}
apps/web/src/{app,features,i18n,shared}
docs/{adr,rfc,architecture}
openspec/{specs,changes}
```

## Comandos

| Objetivo | Comando |
|---|---|
| Instalar tudo + hooks | `make setup` |
| Todas as verificações (igual ao CI) | `make check` |
| Testes | `make test` |
| API em dev | `make api-dev` (requer `make db-up`) |
| Web em dev | `make web-dev` |
| Validar specs | `make specs` |

## Antes de concluir uma tarefa

- `make check` verde.
- Tarefas do `tasks.md` marcadas; specs OpenSpec coerentes com o comportamento implementado.
