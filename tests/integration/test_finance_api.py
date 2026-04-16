import pytest
from src.apis.apis.finance.app import app


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client


def test_finance_api_response_check_auth(client, finance_api_bearer_token):
    headers = {"Authorization": f"Bearer {finance_api_bearer_token}"}
    response = client.get("/auth/status", headers=headers)

    assert response.status_code == 200
    assert response.json.get("status") == "ok"