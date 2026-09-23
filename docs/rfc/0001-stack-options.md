# RFC-0001: Levantamento de opções de frontend e backend

- **Status:** Aceita
- **Autor(es):** Hitomi Growth + Claude Code
- **Criada em:** 2026-09-23
- **ADRs resultantes:** [ADR-0002](../adr/0002-backend-fastapi.md), [ADR-0003](../adr/0003-frontend-react-vite.md), [ADR-0004](../adr/0004-modular-monolith-ddd.md)

## Resumo

Compara stacks de backend e frontend para um app de gestão financeira pessoal
(PF + PJ) com requisitos de segurança (JWT, login social, MFA), DDD, monólito
modular com caminho para microsserviços, i18n, TDD e suporte a agentes de IA.

## Critérios

1. **Adequação a DDD / monólito modular** — facilidade de isolar bounded contexts e verificar fronteiras.
2. **Segurança de autenticação** — bibliotecas maduras para JWT, OAuth2/OIDC, TOTP, hashing de senha.
3. **Testabilidade** — ergonomia de TDD, velocidade da suíte.
4. **Contrato de API** — geração de OpenAPI (importante para o front e para agentes de IA).
5. **Evolução para IA** — facilidade de acoplar previsão, classificação e agentes.
6. **Custo operacional** — projeto pessoal, uma pessoa mantendo.

## Backend

| Opção | DDD / modular | Auth | TDD | OpenAPI | IA | Custo |
|---|---|---|---|---|---|---|
| **FastAPI + Python** | Bom (pacotes + import-linter para fronteiras) | Bom (pyjwt, argon2-cffi, authlib, pyotp) | Excelente (pytest) | Nativo, automático | **Excelente** (ecossistema de dados/ML/LLM) | Baixo |
| NestJS + TypeScript | Excelente (módulos nativos) | Excelente (Passport) | Bom (Jest/Vitest) | Via decorators | Bom | Baixo; tipos compartilhados com o front |
| Spring Boot + Kotlin | Excelente (Spring Modulith verifica módulos) | Excelente (Spring Security) | Bom | springdoc | Médio | Alto (JVM, verbosidade) |
| Go (chi/echo) | Médio (tudo na mão) | Médio | Bom | Via geradores | Médio | Baixo em runtime, alto em código |

## Frontend

| Opção | Client/server limpo | i18n | Testes | Observação |
|---|---|---|---|---|
| **React + Vite (SPA)** | **Sim** — só consome a API | react-i18next | Vitest + Testing Library | Hospedagem estática, ecossistema enorme |
| Next.js | Parcial — servidor no front borra a fronteira | next-intl | Vitest/Playwright | SSR/SEO desnecessários em app autenticado |
| Angular | Sim | Nativo | Jasmine/Jest | Mais cerimônia |
| Vue 3 + Vite | Sim | vue-i18n | Vitest | Ecossistema menor |

## Arquitetura: monólito modular × microsserviços

Os requisitos citam os dois. Proposta aceita: **monólito modular primeiro**, com
bounded contexts isolados e comunicação por interfaces de aplicação ou eventos de
domínio. Um contexto só vira microsserviço quando houver motivo concreto
(escala, ciclo de deploy ou linguagem diferente — ex.: motor de previsão ou
agente de IA). As fronteiras verificadas por ferramenta tornam essa extração
barata. Detalhes em [ADR-0004](../adr/0004-modular-monolith-ddd.md).

## Decisão

Escolhida pelo dono do produto em 2026-09-23:

- Backend: **FastAPI + Python**
- Frontend: **React + Vite SPA (TypeScript)**
- Arquitetura: **monólito modular primeiro**
- Login social: **Google, Microsoft, GitHub**

## Fora de escopo

App mobile nativo (candidato a RFC futura). Open Finance passou a ser tratado na [RFC-0004](0004-open-finance.md).
