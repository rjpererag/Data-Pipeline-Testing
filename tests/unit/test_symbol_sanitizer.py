import pytest
from src.processors.symbol_sanitizer import SymbolSanitizer


@pytest.fixture()
def sanitizer(symbols):
    return SymbolSanitizer(symbols)


@pytest.mark.parametrize(
    "symbol, expected", [
        ("usd ", "USD"),
        (" Eur ", "EUR"),
        (" GbP", "GBP"),
    ])
def test_symbol_sanitizer(
        sanitizer: SymbolSanitizer,
        symbol,
        expected,
):
    new_symbol = sanitizer.sanitize(symbol)
    assert new_symbol == expected


def test_symbol_sanitizer_invalid_type(sanitizer):
    """Verify that non-string inputs (like integers or None) raise TypeError."""
    with pytest.raises(TypeError, match="not a valid string"):
        sanitizer.sanitize(123)

    with pytest.raises(TypeError):
        sanitizer.sanitize(None)


def test_symbol_sanitizer_not_found(sanitizer):
    """Verify that symbols not in our 'allowed list' raise ValueError."""
    with pytest.raises(ValueError, match="Symbol not found"):
        sanitizer.sanitize("BTC")  # Assuming BTC isn't in your fixture