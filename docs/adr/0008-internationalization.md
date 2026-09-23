# ADR-0008: Internacionalização (en-US, pt-BR)

- **Status:** Aceito
- **Data:** 2026-09-23

## Decisão

- Locales suportados: **`pt-BR`** (padrão) e **`en-US`**.
- **Frontend:** react-i18next, arquivos `apps/web/src/i18n/locales/<locale>/<namespace>.json`; datas/moedas com `Intl`. Um teste garante que todos os locales têm as mesmas chaves.
- **Backend:** mensagens de erro retornam um **código estável** (`error.code`, ex.: `auth.invalid_credentials`) + mensagem traduzida conforme `Accept-Language` (fallback `pt-BR`). O front deve preferir traduzir pelo código.
- Preferência de idioma salva no perfil do usuário (a partir do contexto `identity`).
- Dados do usuário (nomes de categorias criadas por ele) **não** são traduzidos; categorias padrão sim, por chave.

## Consequências

- Todo texto visível passa por chave de tradução; lint/revisão rejeitam strings literais em JSX.
