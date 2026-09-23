from typing import Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from finance_api.core.config import Settings, get_settings

router = APIRouter(tags=["platform"])


class HealthResponse(BaseModel):
    status: Literal["ok"]
    version: str


@router.get("/health", response_model=HealthResponse)
async def health(settings: Settings = Depends(get_settings)) -> HealthResponse:  # noqa: B008
    return HealthResponse(status="ok", version=settings.version)
