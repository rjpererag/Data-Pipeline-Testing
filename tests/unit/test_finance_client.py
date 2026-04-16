import responses
import pytest
from src.apis.clients.finance import FinanceAPIClient
from src.apis.apis.finance.functions.price import get_random_price
from src.apis.clients.dataclasses.prices import Price
from pydantic import ValidationError


@responses.activate
def test_client_authentication_flow(finance_api_bearer_token):
    mock_url = "http://fake-api.com/auth/status"
    responses.add(
        responses.GET,
        mock_url,
        json={"status": "ok"},
        status=200,
    )

    client = FinanceAPIClient(
        base_url="http://fake-api.com",
        token=finance_api_bearer_token
    )
    is_authenticated  = client.check_auth()
    assert is_authenticated == True
    assert responses.calls[0].request.headers["Authorization"] == "Bearer secret-123"


@pytest.fixture
@responses.activate
def client(finance_api_bearer_token) -> FinanceAPIClient:
    mock_url = "http://fake-api.com/auth/status"
    responses.add(
        responses.GET,
        mock_url,
        json={"status": "ok"},
        status=200,
    )

    client = FinanceAPIClient(
        base_url="http://fake-api.com",
        token=finance_api_bearer_token
    )
    client.authenticate()
    return client


@responses.activate
def test_get_price(client):
    mock_url = "http://fake-api.com/prices"
    responses.add(
        responses.GET,
        f"{mock_url}/btc",
        json=get_random_price(symbol="btc"),
        status=200,
    )

    price = client.get_price(symbol="btc")
    assert isinstance(price, dict)


@pytest.mark.parametrize(
    "symbol, price, expected", [
        ("btc", 1000, Price(symbol="btc", price=1000)),
        ("btc", "2000.0", Price(symbol="btc", price=2000.0)),
    ])
def test_parse_price_success(
        client,
        symbol: str,
        price: float,
        expected: Price
):
    price_response = {
        "symbol": symbol,
        "price": price,
    }

    parsed_price = client.parse_price(price=price_response, symbol=symbol)
    assert parsed_price == expected

@pytest.mark.parametrize(
    "symbol, price, expected", [
        ("btc", None, Price(symbol="btc", price=1000)),
        (None, "2000.0", Price(symbol="btc", price=2000.0)),
    ])
def test_parse_price_failure(
        client,
        symbol: str,
        price: float,
        expected: Price
):

    with pytest.raises(ValueError, match="Data integrity error for"):
        price_response = {"symbol": symbol, "price": price}
        client.parse_price(price=price_response, symbol=symbol)
