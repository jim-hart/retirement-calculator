from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from retirement_calculator.models import User


@pytest.fixture
def mock_user(mock_user_data) -> User:
    """
    :returns:   A User instance created from mocked data.
    """
    return User.parse_obj(mock_user_data)


@pytest.mark.parametrize(
    "field",
    (
        "current_savings_rate",
        "expected_rate_of_return",
        "pre_retirement_income_percent",
    ),
)
def test_written_percentages_converted_to_float(field: str, mock_user_data: dict):
    user = User.model_validate(mock_user_data)
    assert getattr(user, field) == mock_user_data[field] / 100


def test_retirement_age_must_be_greater_than_current_age(mock_user_data: dict):
    date_of_birth = date.fromisoformat(mock_user_data["date_of_birth"])
    delta = date.today() - date_of_birth
    mock_user_data["retirement_age"] = delta.days // 365
    with pytest.raises(ValidationError):
        User.model_validate(mock_user_data)


def test_life_expectancy_must_be_greater_than_retirement_age(mock_user_data: dict):
    mock_user_data["life_expectancy"] = mock_user_data["retirement_age"]
    with pytest.raises(ValidationError):
        User.model_validate(mock_user_data)


def test_current_age_matches_expected_value(mock_user_data: dict):
    """
    Verify User.current_age is correctly calculated using User.date_of_birth
    """
    expected_age = 50
    date_of_birth = age_to_date_of_birth(expected_age)
    mock_user_data["date_of_birth"] = date_of_birth.isoformat()
    user = User.model_validate(mock_user_data)
    assert user.current_age == expected_age


def test_calculated_years_to_retirement_matches_expected_value(mock_user_data: dict):
    user = User.model_validate(mock_user_data)
    expected_years = mock_user_data["retirement_age"] - user.current_age
    assert user.years_to_retirement == expected_years


def test_calculated_years_in_retirement_matches_expected_value(mock_user_data: dict):
    user = User.model_validate(mock_user_data)
    expected_years = (
        mock_user_data["life_expectancy"] - mock_user_data["retirement_age"]
    )
    assert user.expected_years_in_retirement == expected_years
