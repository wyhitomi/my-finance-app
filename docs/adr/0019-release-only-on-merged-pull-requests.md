# ADR-0019: Release-please roda somente no merge de pull request na `main`

- **Status:** Aceito
- **Data:** 2026-09-23
- **Relacionados:** ADR-0017 (ajusta o gatilho), ADR-0010

## Contexto

O ADR-0017 definiu que o workflow do release-please roda "a cada push na `main`", e ele
também aceitava disparo manual (`workflow_dispatch`). O dono do produto decidiu que o
release-please deve rodar **somente quando um merge é feito para a `main`**.

## Decisão

1. O workflow `Release` é disparado apenas pelo evento `pull_request` do tipo `closed`
   com base `main`, e o job só executa se o PR foi **mergeado**
   (`github.event.pull_request.merged == true`). PRs fechados sem merge não disparam nada.
2. Push direto na `main` e disparo manual **não** acionam o release-please.
3. A branch alvo fica fixa (`target-branch: main`), sem depender da detecção automática.
4. As imagens versionadas são construídas a partir do **commit de merge**
   (`merge_commit_sha`), repassado ao `cd.yml`. No evento de PR, o commit padrão do
   workflow seria a referência temporária do PR, e não o commit que entrou na `main`.
   Essas imagens recebem só as tags `X.Y.Z` e `X.Y`. A tag por SHA e a `latest` continuam
   vindo do CD que roda em todo push na `main`.

## Alternativas consideradas

| Opção | Por que não |
|---|---|
| Manter `push` na `main` | Também dispararia em push direto, contra a decisão. |
| Manter `workflow_dispatch` como escape manual | Contraria o "somente no merge". Para recriar um PR de release, basta fechá-lo: o próximo merge na `main` abre um novo. |

## Consequências

- O PR de release só é aberto ou atualizado depois de um merge na `main`.
- Sem disparo manual, recriar um PR de release exige fechá-lo e esperar o próximo merge.
- O CD de imagens por commit (`cd.yml` em push na `main`) não muda.
