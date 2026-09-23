from starlette.datastructures import Headers, MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from finance_api.core.i18n import negotiate_locale, use_locale


class LocaleMiddleware:
    """Resolves the request locale and sets the Content-Language response header."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        locale = negotiate_locale(Headers(scope=scope).get("accept-language"))

        async def send_with_language(message: Message) -> None:
            if message["type"] == "http.response.start":
                MutableHeaders(scope=message)["Content-Language"] = locale
            await send(message)

        with use_locale(locale):
            await self.app(scope, receive, send_with_language)
