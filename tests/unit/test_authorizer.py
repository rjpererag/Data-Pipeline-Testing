import pytest
from unittest.mock import MagicMock
from src.apis.apis.finance.authorizer import Authorizer, Authorization
from src.apis.apis.finance.db_model.user_db_manager import DBUserManager, User


@pytest.fixture
def mock_manager():
    return MagicMock(spec=DBUserManager)


@pytest.fixture
def auth(mock_manager):
    return Authorizer(db_manager=mock_manager)


def test_check_auth_invalid_token_type(auth):
    result = auth.check_auth(bearer_token=None)
    assert result.status_code == 400
    assert result.is_authorized is False
    assert "Invalid bearer token" in result.error

def test_check_auth_unauthorized(auth, mock_manager):
    mock_manager.get_user_by_token.return_value = None
    result = auth.check_auth(bearer_token="bad-token")

    assert result.status_code == 401
    assert result.is_authorized is False
    assert "Unauthorized" in result.error

def test_check_auth_success(auth, mock_manager):
    mock_user = MagicMock(spec=User)
    mock_user.is_active = True
    mock_manager.get_user_by_token.return_value = mock_user

    result = auth.check_auth(bearer_token="valid-token")
    assert result.status_code == 200
    assert result.is_authorized is True
    assert result.error is None


def test_check_auth_system_error(auth, mock_manager):
    mock_manager.get_user_by_token.side_effect = Exception("DB Connection Timeout")

    result = auth.check_auth(bearer_token="any-token")
    assert result.status_code == 500
    assert "System error" in result.error