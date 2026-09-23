# ADR-0006: Autenticação com JWT, senha Argon2id, OAuth2/OIDC e MFA TOTP

- **Status:** Aceito (detalhes de fluxo em discussão na RFC-0003)
- **Data:** 2026-09-23
- **Relacionados:** RFC-0003

## Decisão

- **Senha:** Argon2id (`argon2-cffi`), política mínima de 12 caracteres, checagem contra senhas vazadas.
- **Login social:** OAuth 2.0 / OpenID Connect com **PKCE** e `state`, via **Authlib**, provedores **Google, Microsoft, GitHub**.
- **Tokens:** access token **JWT** de 15 min (assinatura assimétrica), refresh token opaco rotativo com detecção de reuso em cookie `HttpOnly`/`Secure`/`SameSite=Strict`.
- **MFA:** TOTP (RFC 6238, `pyotp`) + códigos de recuperação; exigido também no login social.
- Access token mantido só em memória no SPA.

## Alternativas consideradas

| Opção | Por que não (agora) |
|---|---|
| Provedor gerenciado (Auth0, Clerk, Cognito, Keycloak) | Menos controle e custo recorrente; mas continua opção se o esforço de segurança crescer — o contexto `identity` isola essa troca. |
| Sessão server-side com cookie | Viável; JWT foi requisito explícito e facilita futuros serviços extraídos validarem tokens sem estado. |

## Consequências

- Revogação imediata de access token não é possível (mitigado pela validade curta).
- Chaves de assinatura precisam de rotação (JWKS em `/api/v1/auth/.well-known/jwks.json`).
