# RFC-0003: Autenticação, login social e MFA

- **Status:** Em discussão
- **Autor(es):** Hitomi Growth + Claude Code
- **Criada em:** 2026-09-23
- **ADRs resultantes:** [ADR-0006](../adr/0006-authentication.md)

## Resumo

Detalha fluxos de autenticação do contexto `identity`: senha, login social
(Google, Microsoft, GitHub via OAuth 2.0/OIDC com PKCE) e MFA (TOTP + códigos
de recuperação), emitindo JWTs de curta duração.

## Fluxos propostos

**Cadastro com senha**
1. `POST /api/v1/auth/register` — e-mail + senha (mín. 12 caracteres, checada contra lista de senhas vazadas).
2. Senha armazenada com **Argon2id**. E-mail de verificação obrigatório antes do primeiro login.

**Login com senha**
1. `POST /api/v1/auth/login` → se MFA ativo, retorna `mfa_token` (JWT de 5 min, escopo `mfa`); senão, tokens de sessão.
2. `POST /api/v1/auth/mfa/verify` com `mfa_token` + código TOTP → tokens de sessão.

**Login social**
1. `GET /api/v1/auth/oauth/{provider}/authorize` → redireciona com `state` + PKCE.
2. `GET /api/v1/auth/oauth/{provider}/callback` → vincula por e-mail **verificado** pelo provedor; nunca vincula automaticamente e-mail não verificado.
3. MFA, se ativo, também é exigido no login social.

**Tokens**
- Access token: JWT assinado (EdDSA/Ed25519 ou RS256), 15 min, enviado em `Authorization: Bearer`.
- Refresh token: opaco, 30 dias, **rotativo** com detecção de reuso (reuso revoga a família inteira), em cookie `HttpOnly; Secure; SameSite=Strict`, path `/api/v1/auth/refresh`.
- Access token fica **apenas em memória** no SPA (não em `localStorage`).

**MFA**
- TOTP (RFC 6238) com QR code; 10 códigos de recuperação de uso único (hash armazenado).
- Passkeys/WebAuthn como evolução futura.

**Proteções**
- Rate limiting e bloqueio progressivo por conta/IP; mensagens de erro genéricas (sem enumeração de usuário).
- Log de auditoria de eventos de segurança (login, falha, MFA ativado, token reusado).

## Perguntas em aberto

- [ ] MFA **obrigatório** para todos, ou opcional (recomendado com aviso)?
- [ ] Envio de e-mail (verificação, reset de senha): qual provedor? (SES, Resend, SMTP próprio)
- [ ] Onde o app será hospedado? Afeta domínio de cookie (SPA e API no mesmo domínio simplificam `SameSite=Strict`).

## Fora de escopo

SSO corporativo (SAML), login por SMS (inseguro), passkeys na primeira versão.
