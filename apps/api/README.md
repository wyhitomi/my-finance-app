# finance-api

FastAPI modular monolith. See [ADR-0002](../../docs/adr/0002-backend-fastapi.md) and [ADR-0004](../../docs/adr/0004-modular-monolith-ddd.md).

```bash
uv sync               # install
uv run pytest         # tests + coverage
uv run lint-imports   # module boundary contracts
uv run uvicorn finance_api.main:app --reload
```
