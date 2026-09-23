# Diagramas de arquitetura

Diagramas em [Mermaid](https://mermaid.js.org/). O GitHub renderiza direto nesta página.
Eles seguem os níveis do [modelo C4](https://c4model.com/): contexto → containers → componentes.
Atualize este arquivo no mesmo PR de qualquer ADR que mude a arquitetura.

**Legenda de cores:** roxo = núcleo do negócio · cinza = suporte · laranja = serviço externo ·
tracejado = assíncrono (eventos/webhooks) ou ainda a definir.

## 1. Contexto do sistema

Quem usa o sistema e com quais serviços externos ele conversa.

```mermaid
flowchart TB
    user(["👤 Usuário<br/>vida financeira PF e PJ"])
    app["<b>My Finance App</b><br/>contas, cartões, lançamentos,<br/>orçamentos e relatórios"]

    idp["Google · Microsoft · GitHub<br/>login social (OIDC)"]
    agg["Agregador Open Finance<br/>(adiado, RFC-0004)"]
    banks[("Bancos<br/>Open Finance Brasil")]
    mail["Provedor de e-mail<br/>(a definir, RFC-0003)"]
    bcb["Banco Central do Brasil<br/>cotações PTAX (RFC-0006)"]

    user -->|"usa no navegador<br/>pt-BR / en-US<br/>envia extratos OFX/CSV"| app
    app <-->|autenticação| idp
    app <-.->|"contas e transações<br/>(ADR-0013, adiado)"| agg
    agg <-->|consentimento e dados| banks
    app -.->|"verificação de e-mail,<br/>troca de senha"| mail
    app -->|cotações diárias| bcb

    classDef system fill:#ede9fe,stroke:#6d28d9,color:#2e1065
    classDef external fill:#fff7ed,stroke:#c2410c,color:#431407
    class app system
    class idp,agg,banks,mail,bcb external
```

## 2. Containers

As peças que rodam separadamente. Decisões: [ADR-0002](../adr/0002-backend-fastapi.md),
[ADR-0003](../adr/0003-frontend-react-vite.md), [ADR-0005](../adr/0005-persistence-postgresql.md),
[ADR-0006](../adr/0006-authentication.md).

```mermaid
flowchart LR
    user(["👤 Usuário"])

    subgraph browser["Navegador"]
        web["<b>apps/web</b><br/>SPA React 19 + Vite + TS<br/>react-i18next · TanStack Query<br/>access token só em memória"]
    end

    subgraph backend["Servidor"]
        api["<b>apps/api</b><br/>FastAPI · Python 3.12<br/>monólito modular<br/>/api/v1 · OpenAPI"]
        db[("<b>PostgreSQL 16</b><br/>um schema por<br/>bounded context")]
    end

    agg["Agregador<br/>Open Finance"]
    idp["Provedores OIDC"]

    user -->|HTTPS| web
    web -->|"REST JSON · Bearer JWT (15 min)<br/>refresh em cookie HttpOnly"| api
    web -.->|widget de consentimento| agg
    api -->|SQLAlchemy 2 async| db
    api <-->|"API + webhooks assinados"| agg
    api <-->|OIDC + PKCE| idp

    classDef container fill:#ede9fe,stroke:#6d28d9,color:#2e1065
    classDef external fill:#fff7ed,stroke:#c2410c,color:#431407
    class web,api,db container
    class agg,idp external
```

## 3. Bounded contexts dentro da API

Como o monólito modular é dividido ([ADR-0004](../adr/0004-modular-monolith-ddd.md),
[RFC-0002](../rfc/0002-domain-model.md), [ADR-0013](../adr/0013-account-sources-and-banking-integration.md)).
Setas cheias são chamadas à camada `application` de outro contexto. Setas tracejadas são
eventos de domínio. Nenhum contexto importa o interior de outro, e o `import-linter`
verifica isso no CI. Todas as requisições entram pela camada HTTP `/api/v1` (JWT,
`Accept-Language`, envelope de erro), que roteia para o `api` de cada contexto.

```mermaid
flowchart TB
    subgraph ctx["Bounded contexts"]
        identity["<b>identity</b><br/>senha · login social<br/>MFA · tokens"]
        accounts["<b>accounts</b><br/>titulares PF/PJ<br/>contas · cartões · faturas<br/>source: manual | open_finance"]
        ledger["<b>ledger</b><br/>lançamentos · parcelas<br/>categorias · conciliação<br/>origin: manual | imported | recurring"]
        budgeting["<b>budgeting</b><br/>orçamentos"]
        reporting["<b>reporting</b><br/>consolidado · previsão"]
        banking["<b>banking_integration</b><br/>camada anticorrupção<br/>importação OFX/CSV (RFC-0005)<br/>Open Finance (adiado)"]
        exchange["<b>exchange</b><br/>cotações PTAX<br/>conversão entre moedas"]
    end

    kernel["<b>shared_kernel</b><br/>Money · Currency · IDs · eventos"]

    identity -->|UserId| accounts
    accounts -->|"AccountId / CardId"| ledger
    banking -->|contas conectadas| accounts
    banking -->|"importa transações"| ledger
    ledger -.->|"TransactionRecorded"| budgeting
    ledger -.->|"TransactionRecorded"| reporting
    budgeting -.->|"BudgetChanged"| reporting
    reporting -->|converte para moeda de referência| exchange
    ledger -->|cotação de referência p/ spread| exchange

    ctx --> kernel

    classDef core fill:#ede9fe,stroke:#6d28d9,color:#2e1065
    classDef support fill:#f3f4f6,stroke:#6b7280,color:#111827
    class accounts,ledger,budgeting,reporting core
    class identity,banking,exchange,kernel support
```

Cada contexto tem as mesmas quatro camadas, e as dependências só apontam para dentro:

```mermaid
flowchart LR
    api["<b>api</b><br/>routers FastAPI"] --> app["<b>application</b><br/>casos de uso · portas<br/>(API pública do módulo)"]
    infra["<b>infrastructure</b><br/>SQLAlchemy · OAuth<br/>adaptador do agregador"] --> app
    app --> domain["<b>domain</b><br/>entidades · value objects<br/>eventos · Python puro"]
    infra -.->|implementa portas| app

    classDef inner fill:#ede9fe,stroke:#6d28d9,color:#2e1065
    classDef outer fill:#f3f4f6,stroke:#6b7280,color:#111827
    class domain,app inner
    class api,infra outer
```

## 4. Fluxos críticos

### Login com senha e MFA ([RFC-0003](../rfc/0003-authentication-and-mfa.md))

```mermaid
sequenceDiagram
    autonumber
    actor U as Usuário
    participant W as apps/web
    participant A as API · identity
    participant D as PostgreSQL

    U->>W: e-mail + senha
    W->>A: POST /auth/login
    A->>D: busca usuário, confere hash Argon2id
    alt MFA ativo
        A-->>W: mfa_token (JWT de 5 min, escopo mfa)
        U->>W: código TOTP
        W->>A: POST /auth/mfa/verify
    end
    A->>D: grava família de refresh tokens
    A-->>W: access token (15 min) + cookie HttpOnly de refresh
    Note over W: access token fica só em memória
    W->>A: chamadas com Authorization: Bearer
    W->>A: POST /auth/refresh (cookie) ao expirar
    A-->>W: novo par de tokens (rotação, reuso revoga a família)
```

### Sincronização Open Finance ([RFC-0004](../rfc/0004-open-finance.md))

```mermaid
sequenceDiagram
    autonumber
    actor U as Usuário
    participant W as apps/web
    participant B as API · banking_integration
    participant G as Agregador
    participant K as Banco
    participant L as accounts / ledger

    U->>W: "Conectar banco" (escolhe titular PF/PJ)
    W->>B: POST /banking/connections
    B->>G: cria token de conexão
    B-->>W: token do widget
    W->>G: abre widget
    G->>K: redireciona para consentimento
    K-->>G: consentimento aprovado
    G-->>B: webhook "conexão criada" (assinatura verificada)
    B->>G: busca contas, cartões e transações
    B->>L: cria/atualiza contas (source = open_finance)
    B->>L: importa transações (idempotente por external_id)
    L-->>L: sugere conciliação com lançamentos manuais
    L-->>U: pede confirmação das conciliações sugeridas
    loop novos dados
        G-->>B: webhook de atualização (+ job periódico de segurança)
        B->>L: importa só o que é novo
    end
```
