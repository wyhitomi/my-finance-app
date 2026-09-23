"""API scenarios from openspec spec `localization`."""

import pytest
from fastapi import APIRouter, FastAPI
from httpx import ASGITransport, AsyncClient

from finance_api.core.config import Settings
from finance_api.core.errors import AppError
from finance_api.main import create_app


@pytest.fixture
def app(settings: Settings) -> FastAPI:
    """App with extra routes that exercise the error handlers."""
    application = create_app(settings)
    router = APIRouter(prefix="/api/v1/_test")

    @router.get("/items/{item_id}")
    async def read_item(item_id: int) -> dict[str, int]:
        return {"id": item_id}

    @router.get("/app-error")
    async def raise_app_error() -> None:
        raise AppError("common.conflict", status_code=409)

    @router.get("/boom")
    async def boom() -> None:
        raise RuntimeError("db password leaked in traceback")

    application.include_router(router)
    return application


@pytest.mark.parametrize(
    ("accept_language", "expected"),
    [
        ("en-US,en;q=0.9", "en-US"),
        ("en-GB", "en-US"),
        ("fr-FR", "pt-BR"),
        (None, "pt-BR"),
        ("fr;q=1.0, en;q=0.8, pt;q=0.5", "en-US"),
    ],
)
async def test_content_language_header(
    client: AsyncClient, accept_language: str | None, expected: str
) -> None:
    headers = {"Accept-Language": accept_language} if accept_language else {}

    response = await client.get("/api/v1/health", headers=headers)

    assert response.headers["Content-Language"] == expected


@pytest.mark.parametrize(
    ("accept_language", "message"),
    [("pt-BR", "Recurso não encontrado."), ("en-US", "Resource not found.")],
)
async def test_unknown_route_returns_localized_error(
    client: AsyncClient, accept_language: str, message: str
) -> None:
    response = await client.get(
        "/api/v1/does-not-exist", headers={"Accept-Language": accept_language}
    )

    assert response.status_code == 404
    assert response.json() == {"error": {"code": "common.not_found", "message": message}}
    assert response.headers["Content-Language"] == accept_language


async def test_validation_errors_use_envelope(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/_test/items/not-an-int", headers={"Accept-Language": "en-US"}
    )

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "common.validation_failed"
    assert body["error"]["message"] == "The request contains invalid data."
    assert body["error"]["details"]


async def test_app_errors_are_translated(client: AsyncClient) -> None:
    response = await client.get("/api/v1/_test/app-error", headers={"Accept-Language": "pt-BR"})

    assert response.status_code == 409
    assert response.json() == {
        "error": {
            "code": "common.conflict",
            "message": "O recurso está em conflito com o estado atual.",
        }
    }


async def test_unexpected_errors_are_hidden(app: FastAPI) -> None:
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/_test/boom", headers={"Accept-Language": "en-US"})

    assert response.status_code == 500
    assert response.json()["error"]["code"] == "common.internal_error"
    assert "db password" not in response.text
