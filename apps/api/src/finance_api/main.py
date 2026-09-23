from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from finance_api.api.v1 import router as v1_router
from finance_api.core.config import Settings, get_settings
from finance_api.core.errors import register_error_handlers
from finance_api.core.i18n.middleware import LocaleMiddleware


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url=None,
    )
    app.dependency_overrides[get_settings] = lambda: settings
    app.add_middleware(LocaleMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Language"],
    )
    register_error_handlers(app)
    app.include_router(v1_router)
    return app


app = create_app()
