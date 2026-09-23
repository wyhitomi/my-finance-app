"""Scenarios from openspec spec `money`."""

from decimal import Decimal

import pytest

from finance_api.shared_kernel.money import (
    Currency,
    CurrencyMismatchError,
    InvalidMoneyError,
    Money,
)


def brl(amount: str) -> Money:
    return Money.of(amount, "BRL")


class TestExactDecimals:
    def test_exact_addition(self) -> None:
        assert brl("0.10") + brl("0.20") == brl("0.30")

    def test_subtraction_and_negation(self) -> None:
        assert brl("10.00") - brl("2.50") == brl("7.50")
        assert -brl("1.00") == brl("-1.00")

    def test_multiplication_by_integer_or_decimal(self) -> None:
        assert brl("10.00") * 3 == brl("30.00")
        assert brl("10.00") * Decimal("0.5") == brl("5.00")

    def test_floats_are_rejected(self) -> None:
        with pytest.raises(InvalidMoneyError):
            Money(0.1, Currency.BRL)  # type: ignore[arg-type]

    def test_float_multiplier_is_rejected(self) -> None:
        with pytest.raises(InvalidMoneyError):
            brl("1.00") * 0.5  # type: ignore[operator]

    def test_non_numeric_string_is_rejected(self) -> None:
        with pytest.raises(InvalidMoneyError):
            Money.of("abc", "BRL")

    def test_non_finite_amount_is_rejected(self) -> None:
        with pytest.raises(InvalidMoneyError):
            Money.of("NaN", "BRL")

    def test_unknown_currency_is_rejected(self) -> None:
        with pytest.raises(InvalidMoneyError):
            Money.of("1.00", "XYZ")

    def test_zero_factory_and_predicates(self) -> None:
        zero = Money.zero(Currency.USD)
        assert zero.is_zero()
        assert brl("-1").is_negative()
        assert not brl("1").is_negative()


class TestCurrencyMismatch:
    def test_adding_different_currencies_fails(self) -> None:
        with pytest.raises(CurrencyMismatchError):
            _ = brl("10.00") + Money.of("10.00", "USD")

    def test_comparing_different_currencies_fails(self) -> None:
        with pytest.raises(CurrencyMismatchError):
            _ = brl("10.00") < Money.of("10.00", "USD")

    def test_ordering_same_currency(self) -> None:
        assert brl("1.00") < brl("2.00")
        assert brl("2.00") >= brl("2.00")

    def test_equality_with_other_types_is_false(self) -> None:
        assert brl("1.00") != "1.00"


class TestRounding:
    @pytest.mark.parametrize(
        ("raw", "expected"),
        [("10.125", "10.12"), ("10.135", "10.14"), ("-10.125", "-10.12")],
    )
    def test_half_even_rounding(self, raw: str, expected: str) -> None:
        assert str(brl(raw).rounded().amount) == expected

    def test_rounding_respects_minor_units(self) -> None:
        assert Currency.BRL.minor_units == 2


class TestSerialization:
    def test_serializes_amount_as_string(self) -> None:
        assert brl("1234.50").to_dict() == {"amount": "1234.50", "currency": "BRL"}

    def test_round_trip(self) -> None:
        payload = {"amount": "99.90", "currency": "USD"}
        assert Money.from_dict(payload).to_dict() == payload


class TestConstruction:
    def test_currency_code_string_is_coerced(self) -> None:
        assert Money(Decimal("1"), "usd") == Money.of("1", Currency.USD)  # type: ignore[arg-type]

    def test_all_comparisons(self) -> None:
        assert brl("1") <= brl("1")
        assert brl("2") > brl("1")
        with pytest.raises(CurrencyMismatchError):
            _ = brl("1") <= Money.of("1", "USD")
        with pytest.raises(CurrencyMismatchError):
            _ = brl("1") > Money.of("1", "USD")
        with pytest.raises(CurrencyMismatchError):
            _ = brl("1") >= Money.of("1", "USD")
        with pytest.raises(CurrencyMismatchError):
            _ = brl("1") - Money.of("1", "USD")

    def test_hashable(self) -> None:
        assert len({brl("1.0"), brl("1.00")}) == 1
