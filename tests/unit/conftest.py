import pytest


@pytest.fixture()
def rates():
    return {"EUR": 1.08, "GBP": 1.27, "JPY": 0.0067}

@pytest.fixture()
def symbols():
    return ["USD", "EUR", "GBP", "JPY"]
