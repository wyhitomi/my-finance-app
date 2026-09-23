# Spec Delta

## Purpose

Makes the product usable in Brazilian Portuguese and US English, on both the API (error messages) and the web interface.

## ADDED Requirements

### Requirement: API negotiates locale
The API SHALL choose the response locale from the `Accept-Language` header among the supported locales `pt-BR` and `en-US`, honouring quality values, matching on language prefix (e.g. `en` or `en-GB` resolve to `en-US`, `pt` or `pt-PT` to `pt-BR`), and falling back to `pt-BR`. Every response SHALL carry a `Content-Language` header with the chosen locale.

#### Scenario: English requested
- **GIVEN** a request with `Accept-Language: en-US,en;q=0.9`
- **WHEN** the API responds
- **THEN** the `Content-Language` header is `en-US`

#### Scenario: Language prefix match
- **GIVEN** a request with `Accept-Language: en-GB`
- **WHEN** the API responds
- **THEN** the `Content-Language` header is `en-US`

#### Scenario: Unsupported or missing language
- **GIVEN** a request with `Accept-Language: fr-FR` or no header
- **WHEN** the API responds
- **THEN** the `Content-Language` header is `pt-BR`

#### Scenario: Quality values are honoured
- **GIVEN** a request with `Accept-Language: fr;q=1.0, en;q=0.8, pt;q=0.5`
- **WHEN** the API responds
- **THEN** the `Content-Language` header is `en-US`

### Requirement: API errors carry a stable code and a localized message
Error responses SHALL use the body `{"error": {"code": "<stable.code>", "message": "<localized text>"}}`. The `code` SHALL NOT vary by locale.

#### Scenario: Unknown route in Portuguese
- **GIVEN** a request with `Accept-Language: pt-BR`
- **WHEN** the client requests a route that does not exist
- **THEN** the status is 404
- **AND** `error.code` is `common.not_found`
- **AND** `error.message` is `Recurso não encontrado.`

#### Scenario: Unknown route in English
- **GIVEN** a request with `Accept-Language: en-US`
- **WHEN** the client requests a route that does not exist
- **THEN** `error.code` is `common.not_found`
- **AND** `error.message` is `Resource not found.`

### Requirement: Web UI is localized
The web app SHALL render all user-facing text from translation keys available in both `pt-BR` and `en-US`, choosing the browser language on first visit (fallback `pt-BR`), letting the user switch language at any time, and remembering the choice on that device.

#### Scenario: Default to Portuguese
- **GIVEN** a browser whose language is not supported
- **WHEN** the user opens the app
- **THEN** the interface is shown in pt-BR (title "Minhas Finanças")

#### Scenario: Switch to English
- **GIVEN** the interface is in pt-BR
- **WHEN** the user selects "English (US)" in the language switcher
- **THEN** the interface is shown in en-US (title "My Finances")
- **AND** the document `lang` attribute is `en-US`

#### Scenario: Translation catalogs are complete
- **WHEN** the translation catalogs are compared
- **THEN** pt-BR and en-US contain exactly the same keys
