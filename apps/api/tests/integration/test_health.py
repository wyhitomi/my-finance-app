"""Scenarios from openspec spec `health-check`."""

import re

from httpx import AsyncClient


async def test_service_is_up(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert re.fullmatch(r"\d+\.\d+\.\d+", body["version"])


async def test_openapi_lists_health_route(client: AsyncClient) -> None:
    response = await client.get("/api/openapi.json")

    assert response.status_code == 200
    assert "/api/v1/health" in response.json()["paths"]
