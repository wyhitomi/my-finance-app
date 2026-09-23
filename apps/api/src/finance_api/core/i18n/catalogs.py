"""API message catalogs keyed by stable codes (ADR-0008). Keep both locales in sync."""

from typing import Final

PT_BR: Final[dict[str, str]] = {
    "common.not_found": "Recurso não encontrado.",
    "common.method_not_allowed": "Método não permitido.",
    "common.validation_failed": "A requisição contém dados inválidos.",
    "common.conflict": "O recurso está em conflito com o estado atual.",
    "common.internal_error": "Ocorreu um erro inesperado. Tente novamente mais tarde.",
}

EN_US: Final[dict[str, str]] = {
    "common.not_found": "Resource not found.",
    "common.method_not_allowed": "Method not allowed.",
    "common.validation_failed": "The request contains invalid data.",
    "common.conflict": "The resource conflicts with its current state.",
    "common.internal_error": "An unexpected error occurred. Please try again later.",
}

CATALOGS: Final[dict[str, dict[str, str]]] = {"pt-BR": PT_BR, "en-US": EN_US}
