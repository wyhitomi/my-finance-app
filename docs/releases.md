# Releases (release-please)

Decisão e regras: [ADR-0017](adr/0017-release-management-with-release-please.md). API e web têm versões,
tags (`api-vX.Y.Z`, `web-vX.Y.Z`) e CHANGELOGs independentes.

## Configuração do token

PRs abertos com o `GITHUB_TOKEN` não disparam o CI, então o PR de release ficaria sem checks. O workflow
`.github/workflows/release-please.yml` usa o primeiro token disponível:

1. **GitHub App** (recomendado): variável `RELEASE_PLEASE_APP_ID` + segredo `RELEASE_PLEASE_APP_PRIVATE_KEY`;
2. **PAT fine-grained**: segredo `RELEASE_PLEASE_TOKEN`;
3. `GITHUB_TOKEN` (fallback, sem CI no PR de release).

Configure **uma** das duas opções abaixo.

### Opção A — GitHub App (recomendado)

Não expira, não depende de uma pessoa e os PRs aparecem como `<nome-do-app>[bot]`, então quem mantém o repo
pode aprová-los.

1. GitHub → foto do perfil → **Settings → Developer settings → GitHub Apps → New GitHub App**.
2. Preencha:
   - **GitHub App name:** único no GitHub, ex. `my-finance-release-bot`;
   - **Homepage URL:** `https://github.com/wyhitomi/my-finance-app`;
   - **Webhook:** desmarque **Active**;
   - **Repository permissions:** `Contents: Read and write`, `Pull requests: Read and write`,
     `Issues: Read and write` (labels do PR de release); `Metadata: Read-only` vem automático;
   - **Where can this GitHub App be installed?** `Only on this account`.
3. **Create GitHub App**. Na página do app, anote o **App ID** (número no topo).
4. Em **Private keys → Generate a private key**: um arquivo `.pem` é baixado. Guarde-o com segurança.
5. Menu lateral **Install App → Install** na sua conta → **Only select repositories** → `my-finance-app` →
   **Install**.
6. No repositório: **Settings → Secrets and variables → Actions**:
   - aba **Variables → New repository variable:** `RELEASE_PLEASE_APP_ID` = App ID;
   - aba **Secrets → New repository secret:** `RELEASE_PLEASE_APP_PRIVATE_KEY` = conteúdo inteiro do `.pem`
     (incluindo as linhas `-----BEGIN/END ... KEY-----`).
7. Apague o `.pem` baixado depois de salvar o segredo (dá para gerar outra chave a qualquer momento).

### Opção B — PAT fine-grained

Mais rápido, porém expira e os PRs saem em seu nome — com branch protection exigindo review, você não
consegue aprovar o próprio PR de release.

1. GitHub → foto do perfil → **Settings → Developer settings → Personal access tokens → Fine-grained tokens
   → Generate new token**.
2. Preencha:
   - **Token name:** `release-please my-finance-app`;
   - **Resource owner:** `wyhitomi`;
   - **Expiration:** até 1 ano (anote a data para renovar);
   - **Repository access:** `Only select repositories` → `my-finance-app`;
   - **Repository permissions:** `Contents: Read and write`, `Pull requests: Read and write`,
     `Issues: Read and write`; `Metadata: Read-only` vem automático.
3. **Generate token** e copie o valor (`github_pat_...`) — ele só aparece uma vez.
4. No repositório: **Settings → Secrets and variables → Actions → Secrets → New repository secret:**
   `RELEASE_PLEASE_TOKEN` = token.

## Demais ajustes no repositório

- **Settings → Actions → General → Workflow permissions:** marque *Allow GitHub Actions to create and approve
  pull requests* (necessário apenas para o fallback com `GITHUB_TOKEN`; inofensivo nas outras opções).
- Se usar squash merge, o título do PR vira o commit: mantenha-o em Conventional Commits.

## Verificando

Após o merge de um `feat:` ou `fix:` na `main`, a aba **Actions → Release** deve abrir o PR
`chore(main): release ...`, e esse PR deve rodar o workflow **CI**. Se o CI não rodar, o workflow caiu no
`GITHUB_TOKEN`: confira nomes e valores da variável/segredos.
