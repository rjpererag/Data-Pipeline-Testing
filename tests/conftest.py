import pytest
import uuid
from datetime import datetime


@pytest.fixture
def sample_exchange_id():
    """Provides a consistent UUID for an exchange."""
    return uuid.uuid4()


@pytest.fixture
def sample_symbol_data():
    """Provides a dictionary representing a symbol record"""
    return {
        "id": uuid.uuid4(),
        "name": "Bitcoin",
        "symbol": "BTC"
    }

@pytest.fixture
def mock_price_record(sample_exchange_id):
    """
    Provides a complete price record.
    Notice how this fixture 'injects' another fixture!
    """
    return {
        "ticker_id": uuid.uuid4(),
        "price": 65000.50,
        "timestamp": datetime.now(),
        "exchange_id": sample_exchange_id
    }


@pytest.fixture()
def finance_api_bearer_token() -> str:
    return "parameta-dev-2026"
