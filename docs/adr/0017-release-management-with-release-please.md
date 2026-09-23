# ADR-0017: Versionamento e releases com release-please

- **Status:** Aceito
- **Data:** 2026-09-23
- **Relacionados:** ADR-0010, ADR-0012

## Contexto

Os commits já seguem Conventional Commits (hook `commit-msg`, ADR-0010), mas as versões de `apps/api`
(`pyproject.toml`) e `apps/web` (`package.json`) são mantidas à mão, não há CHANGELOG nem tags, e o CD publica
imagens apenas com `sha` e `latest`. Precisamos de versões semânticas rastreáveis para cada app do monorepo
(ADR-0012) sem trabalho manual.

## Decisão

Vamos usar o **release-please** (`googleapis/release-please-action`) em modo manifest:

- `release-please-config.json` declara dois componentes: `apps/api` (`release-type: python`, tag `api-vX.Y.Z`)
  e `apps/web` (`release-type: node`, tag `web-vX.Y.Z`); `.release-please-manifest.json` guarda a versão atual.
- A cada push na `main`, `.github/workflows/release-please.yml` abre/atualiza **um único PR de release** com o
  bump de versão e o `CHANGELOG.md` de cada app afetado. Ao mesclar esse PR, cria as tags e as GitHub Releases.
- Regras de bump (SemVer): `feat` → minor, `fix`/`perf` → patch, `!`/`BREAKING CHANGE` → major. Enquanto
  estivermos em `0.x`, breaking changes sobem o minor (`bump-minor-pre-major`).
- O CHANGELOG mostra Funcionalidades, Correções, Desempenho e Reversões; os demais tipos (`docs`, `spec`,
  `test`, `ci`, `chore`...) ficam ocultos.
- Após a release, o workflow chama o `cd.yml` (agora também `workflow_call`) para publicar a imagem do app com
  as tags `X.Y.Z` e `X.Y` no GHCR, além de `sha`/`latest`.
- A API expõe a versão lida dos metadados do pacote (`importlib.metadata`), então o bump do `pyproject.toml`
  basta para o `/health` refletir a release.

## Alternativas consideradas

| Opção | Prós | Contras |
|---|---|---|
| release-please | PR de release revisável; suporte nativo a monorepo, Python e Node; sem segredos extras para funcionar | Exige token extra para o PR de release disparar o CI |
| semantic-release | Muito popular no ecossistema JS | Publica direto no merge, sem PR revisável; monorepo e Python via plugins de terceiros |
| Changesets | Ótimo para monorepos JS | Exige arquivo de changeset manual por PR; não cobre Python |
| Versionamento manual | Nenhuma ferramenta | Propenso a erro; sem CHANGELOG |

## Consequências

- Mensagens de commit passam a determinar versões e CHANGELOG: o tipo correto (`feat`, `fix`...) importa. Em
  squash merge, o título do PR vira o commit e também deve seguir Conventional Commits.
- Nunca edite à mão as versões em `pyproject.toml`, `package.json`, os `CHANGELOG.md` nem o manifest.
- Configuração manual no GitHub: em *Settings → Actions → General*, permitir que o GitHub Actions crie PRs.
  PRs abertos com o `GITHUB_TOKEN` não disparam o CI; para o PR de release rodar os checks exigidos pela branch
  protection, cadastre o segredo `RELEASE_PLEASE_TOKEN` (PAT fine-grained ou token de GitHub App com
  `contents` e `pull-requests` de escrita). Sem ele, o workflow usa o `GITHUB_TOKEN`.
- O `uv.lock` continua registrando a versão antiga do próprio projeto após o bump; é inofensivo com
  `uv sync --frozen` e se corrige no próximo `uv lock`.
- `apps/web/CHANGELOG.md` fica fora do Prettier, pois é gerado.
