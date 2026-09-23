"""Error envelope: {"error": {"code", "message", "details"?}} (ADR-0008)."""

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from finance_api.core.i18n import negotiate_locale, translate

logger = logging.getLogger(__name__)

_HTTP_STATUS_CODES = {404: "common.not_found", 405: "common.method_not_allowed"}


class AppError(Exception):
    """Base error for application/use-case failures, identified by a stable code."""

    def __init__(self, code: str, status_code: int = 400) -> None:
        super().__init__(code)
        self.code = code
        self.status_code = status_code


def _envelope(request: Request, status_code: int, code: str, details: Any = None) -> JSONResponse:
    locale = negotiate_locale(request.headers.get("accept-language"))
    error: dict[str, Any] = {"code": code, "message": translate(code, locale)}
    if details is not None:
        error["details"] = jsonable_encoder(details)
    return JSONResponse({"error": error}, status_code, headers={"Content-Language": locale})


async def _app_error(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, AppError)  # noqa: S101
    return _envelope(request, exc.status_code, exc.code)


async def _http_error(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, StarletteHTTPException)  # noqa: S101
    code = _HTTP_STATUS_CODES.get(exc.status_code, "common.internal_error")
    return _envelope(request, exc.status_code, code)


async def _validation_error(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)  # noqa: S101
    return _envelope(request, 422, "common.validation_failed", details=exc.errors())


async def _unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error", exc_info=exc)
    return _envelope(request, 500, "common.internal_error")


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, _app_error)
    app.add_exception_handler(StarletteHTTPException, _http_error)
    app.add_exception_handler(RequestValidationError, _validation_error)
    app.add_exception_handler(Exception, _unexpected_error)
