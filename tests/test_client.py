from unittest.mock import Mock

import pytest
import requests
import requests_cache

from retirement_calculator.client import get_user_data, USER_API_ROOT
from retirement_calculator.models import User


@pytest.fixture(autouse=True)
def disable_http_caching(monkeypatch):
    """
    Temporarily disable HTTP caching, so it doesn't interfere with our tests.
    """
    requests_cache.patcher.disabled()
    yield
    requests_cache.patcher.enabled()


@pytest.fixture
def mock_api_data(mock_user_data):
    """
    :returns:   Data in the format as returned by the users API.
    """
    data = mock_user_data
    return {
        "user_info": {
            "date_of_birth": data["date_of_birth"],
            "household_income": data["household_income"],
            "current_savings_rate": data["current_savings_rate"],
            "current_retirement_savings": data["current_retirement_savings"],
            "full_name": data["full_name"],
            "address": data["address"],
        },
        "assumptions": {
            "pre_retirement_income_percent": data["pre_retirement_income_percent"],
            "life_expectancy": data["life_expectancy"],
            "expected_rate_of_return": data["expected_rate_of_return"],
            "retirement_age": data["retirement_age"],
        },
    }


@pytest.fixture
def mock_get_request(monkeypatch, mock_api_data) -> Mock:
    """
    :returns:   The Mock instance used to patch "requests.get".
    """
    mock_resp = Mock()
    mock_resp.json.return_value = mock_api_data

    mock_get = Mock(return_value=mock_resp)
    monkeypatch.setattr(requests, "get", mock_get)

    return mock_get


def test_type_error_raised_if_using_non_integer_id():
    with pytest.raises(TypeError):
        get_user_data(user_id="1")


def test_expected_url_passed_to_request(mock_get_request):
    get_user_data(user_id=1)
    expected_url = USER_API_ROOT / str(1)
    mock_get_request.assert_called_with(expected_url)


def test_returned_user_model_matches_expected_values(mock_get_request, mock_user_data):
    user1 = get_user_data(user_id=1)
    user2 = User.model_validate(mock_user_data)
    assert user1.model_dump() == user2.model_dump()
