import pytest
from src.processors.fx_converter import FXConverter


@pytest.fixture()
def converter(rates):
    return FXConverter(rates=rates)


@pytest.mark.parametrize("amount, currency, expected", [
    (100.0, "USD", 100.00),
    (100.0, "EUR", 108.0),
    (50.0, "GBP", 63.5),
    (1500.0, "JPY", 10.05),
])
def test_convert_to_usd_success(
        converter: FXConverter,
        amount: float,
        currency: str,
        expected: float
):
    result = converter.convert_to_usd(amount, currency)
    assert result == expected


def test_convert_to_usd_missing_rate(converter: FXConverter):
    with pytest.raises(ValueError, match="No exchange rate found for"):
        converter.convert_to_usd(100.0, "BTC")