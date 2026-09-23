import pytest

from finance_api.core.i18n import (
    DEFAULT_LOCALE,
    SUPPORTED_LOCALES,
    negotiate_locale,
    translate,
    use_locale,
)
from finance_api.core.i18n.catalogs import CATALOGS


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("en-US,en;q=0.9", "en-US"),
        ("en-GB", "en-US"),
        ("en", "en-US"),
        ("pt-PT", "pt-BR"),
        ("pt", "pt-BR"),
        ("PT-br", "pt-BR"),
        ("fr-FR", "pt-BR"),
        ("", "pt-BR"),
        (None, "pt-BR"),
        ("fr;q=1.0, en;q=0.8, pt;q=0.5", "en-US"),
        ("pt;q=0.9, en;q=0.1", "pt-BR"),
        ("en;q=0, pt;q=0.5", "pt-BR"),
        ("*", "pt-BR"),
        ("en;q=abc", "en-US"),
    ],
)
def test_negotiate_locale(header: str | None, expected: str) -> None:
    assert negotiate_locale(header) == expected


def test_default_locale_is_portuguese() -> None:
    assert DEFAULT_LOCALE == "pt-BR"
    assert set(SUPPORTED_LOCALES) == {"pt-BR", "en-US"}


def test_catalogs_have_identical_keys() -> None:
    keys = {locale: set(messages) for locale, messages in CATALOGS.items()}
    assert set(keys) == set(SUPPORTED_LOCALES)
    assert keys["pt-BR"] == keys["en-US"]


def test_translate_uses_current_locale() -> None:
    with use_locale("en-US"):
        assert translate("common.not_found") == "Resource not found."
    assert translate("common.not_found") == "Recurso não encontrado."


def test_translate_unknown_code_returns_code() -> None:
    assert translate("missing.code") == "missing.code"
