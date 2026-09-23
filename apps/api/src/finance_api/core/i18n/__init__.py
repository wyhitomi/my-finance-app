"""Locale negotiation and message translation (ADR-0008).

Framework-free: the current locale lives in a ContextVar set by the HTTP
middleware, so application code can translate without importing FastAPI.
"""

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Final

from finance_api.core.i18n.catalogs import CATALOGS

DEFAULT_LOCALE: Final = "pt-BR"
SUPPORTED_LOCALES: Final = ("pt-BR", "en-US")
_BY_LANGUAGE: Final = {locale.split("-")[0]: locale for locale in SUPPORTED_LOCALES}

_current_locale: ContextVar[str] = ContextVar("current_locale", default=DEFAULT_LOCALE)


def _parse_quality(params: list[str]) -> float:
    for param in params:
        key, _, value = param.strip().partition("=")
        if key.strip() == "q":
            try:
                return float(value)
            except ValueError:
                return 1.0
    return 1.0


def negotiate_locale(accept_language: str | None) -> str:
    """Pick the best supported locale for an Accept-Language header value."""
    if not accept_language:
        return DEFAULT_LOCALE
    candidates: list[tuple[float, int, str]] = []
    for index, part in enumerate(accept_language.split(",")):
        tag, *params = part.strip().split(";")
        quality = _parse_quality(params)
        if tag and quality > 0:
            # Negative index keeps header order stable among equal qualities.
            candidates.append((quality, -index, tag.strip().lower()))
    for _, _, tag in sorted(candidates, reverse=True):
        exact = next((loc for loc in SUPPORTED_LOCALES if loc.lower() == tag), None)
        if exact:
            return exact
        if match := _BY_LANGUAGE.get(tag.split("-")[0]):
            return match
    return DEFAULT_LOCALE


def get_locale() -> str:
    return _current_locale.get()


@contextmanager
def use_locale(locale: str) -> Iterator[None]:
    token = _current_locale.set(locale)
    try:
        yield
    finally:
        _current_locale.reset(token)


def translate(code: str, locale: str | None = None) -> str:
    """Return the message for `code` in `locale` (default: current), or the code itself."""
    catalog = CATALOGS.get(locale or get_locale(), CATALOGS[DEFAULT_LOCALE])
    return catalog.get(code, code)


__all__ = [
    "DEFAULT_LOCALE",
    "SUPPORTED_LOCALES",
    "get_locale",
    "negotiate_locale",
    "translate",
    "use_locale",
]
