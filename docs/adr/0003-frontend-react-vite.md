# ADR-0003: Frontend SPA em React + Vite + TypeScript

- **Status:** Aceito
- **Data:** 2026-09-23
- **Relacionados:** RFC-0001, ADR-0008

## Contexto

O app é inteiramente autenticado (sem necessidade de SEO) e queremos uma
fronteira client/server nítida: o front só conversa com a API.

## Decisão

- **React 19 + Vite + TypeScript (strict)**, gerenciado com **pnpm**.
- Roteamento: **React Router**. Estado de servidor: **TanStack Query**.
- i18n: **react-i18next** (ver ADR-0008).
- Testes: **Vitest + Testing Library**; E2E com **Playwright** (a partir das primeiras telas reais).
- Lint/format: **ESLint** (flat config) + **Prettier**.
- Cliente da API gerado do OpenAPI do backend (a definir na primeira feature que consumir a API).

## Consequências

- Deploy como arquivos estáticos (CDN ou servido pelo mesmo domínio da API).
- Sem SSR: primeira carga depende de JS (aceitável para app autenticado).
