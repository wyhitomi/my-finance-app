# finance-web

React + Vite SPA. See [ADR-0003](../../docs/adr/0003-frontend-react-vite.md) and [ADR-0008](../../docs/adr/0008-internationalization.md).

```bash
pnpm install
pnpm dev            # http://localhost:5173 (proxies /api to :8000)
pnpm test           # Vitest
pnpm lint && pnpm typecheck
```

Translations live in `src/i18n/locales/<locale>/common.json`; a test fails if locales drift apart.
