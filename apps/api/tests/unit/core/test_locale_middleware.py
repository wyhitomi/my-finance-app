from starlette.types import Message, Receive, Scope, Send

from finance_api.core.i18n.middleware import LocaleMiddleware


async def test_non_http_scopes_pass_through() -> None:
    seen: list[str] = []

    async def inner(scope: Scope, receive: Receive, send: Send) -> None:
        seen.append(scope["type"])

    async def receive() -> Message:
        return {"type": "lifespan.startup"}

    async def send(message: Message) -> None:
        return None

    await LocaleMiddleware(inner)({"type": "lifespan"}, receive, send)

    assert seen == ["lifespan"]
