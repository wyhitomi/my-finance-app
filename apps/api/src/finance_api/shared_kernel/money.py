"""Money value object (ADR-0007). Never use float for monetary amounts."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation
from enum import StrEnum
from typing import Self


class InvalidMoneyError(ValueError):
    """Raised when a monetary amount or currency is invalid."""


class CurrencyMismatchError(ValueError):
    """Raised when operating on amounts with different currencies."""


class Currency(StrEnum):
    """Enabled ISO 4217 currencies. Extend when multi-currency is decided (RFC-0002)."""

    BRL = "BRL"
    USD = "USD"
    EUR = "EUR"

    @property
    def minor_units(self) -> int:
        return 2

    @classmethod
    def parse(cls, code: str) -> Currency:
        try:
            return cls(code.upper())
        except ValueError as exc:
            raise InvalidMoneyError(f"Unsupported currency: {code!r}") from exc


def _to_decimal(value: object) -> Decimal:
    # bool is an int subclass and float loses precision: both are rejected.
    if isinstance(value, bool | float) or not isinstance(value, Decimal | int | str):
        raise InvalidMoneyError(f"Monetary amounts must be Decimal, int or str, got {value!r}")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise InvalidMoneyError(f"Invalid monetary amount: {value!r}") from exc
    if not result.is_finite():
        raise InvalidMoneyError(f"Monetary amount must be finite: {value!r}")
    return result


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: Currency

    def __post_init__(self) -> None:
        object.__setattr__(self, "amount", _to_decimal(self.amount))
        if not isinstance(self.currency, Currency):
            object.__setattr__(self, "currency", Currency.parse(str(self.currency)))

    @classmethod
    def of(cls, amount: Decimal | int | str, currency: str | Currency) -> Self:
        return cls(_to_decimal(amount), Currency.parse(str(currency)))

    @classmethod
    def zero(cls, currency: Currency) -> Self:
        return cls(Decimal(0), currency)

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Self:
        return cls.of(data["amount"], data["currency"])

    def to_dict(self) -> dict[str, str]:
        return {"amount": str(self.amount), "currency": self.currency.value}

    def rounded(self) -> Money:
        quantum = Decimal(1).scaleb(-self.currency.minor_units)
        return Money(self.amount.quantize(quantum, rounding=ROUND_HALF_EVEN), self.currency)

    def is_zero(self) -> bool:
        return self.amount.is_zero()

    def is_negative(self) -> bool:
        return self.amount < 0

    def _check_same_currency(self, other: Money) -> None:
        if self.currency is not other.currency:
            raise CurrencyMismatchError(f"{self.currency} != {other.currency}")

    def __add__(self, other: Money) -> Money:
        self._check_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: Money) -> Money:
        self._check_same_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __neg__(self) -> Money:
        return Money(-self.amount, self.currency)

    def __mul__(self, factor: Decimal | int) -> Money:
        return Money(self.amount * _to_decimal(factor), self.currency)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.currency is other.currency and self.amount == other.amount

    def __hash__(self) -> int:
        return hash((self.amount, self.currency))

    def __lt__(self, other: Money) -> bool:
        self._check_same_currency(other)
        return self.amount < other.amount

    def __le__(self, other: Money) -> bool:
        self._check_same_currency(other)
        return self.amount <= other.amount

    def __gt__(self, other: Money) -> bool:
        self._check_same_currency(other)
        return self.amount > other.amount

    def __ge__(self, other: Money) -> bool:
        self._check_same_currency(other)
        return self.amount >= other.amount
