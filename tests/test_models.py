from datetime import date, timedelta
from typing import Final

import pytest
from pydantic import ValidationError

from retirement_calculator.models import User

ANNUAL_SALARY_INCREASE: Final[float] = 0.02

INFLATION_RATE: Final[float] = 0.03


def age_to_date_of_birth(age: int) -> date:
    """
    :returns:   A date that is approximately <age> years from the date this function is
                called.  The dates themselves are slightly padded and should only be
                used for approximate age calculations (e.g. "User is <age> years old").
    """
    age_delta = timedelta(days=(age * 365) + 30)
    return date.today() - age_delta


@pytest.fixture
def mock_calculation_data(mock_user_data: dict) -> dict:
    """
    :returns:   <mock_user_data> with the explicitly set values used for manual
                calculations in model tests. They are explicitly defined here so we
                don't have to recalculate new expected values if we need to alter the
                global values defined in our shared mock_user_data fixture.
    """
    date_of_birth = age_to_date_of_birth(age=30)
    mock_user_data.update(
        current_savings_rate=10,
        household_income=60_000,
        curent_retirement_savings=10_000,
        pre_retirement_income_percent=67,
        life_expectancy=90,
        expected_rate_of_return=10,
        retirement_age=60,
        date_of_birth=date_of_birth.isoformat(),
    )
    return mock_user_data


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


def test_calculated_retirement_income_matches_expected_value(
    mock_calculation_data: dict,
):
    # Manually calculated value using values from mock_calculation_data
    expected_value = 72_817
    user = User.model_validate(mock_calculation_data)
    calculated_value = user.calculate_required_retirement_income(
        annual_salary_increase=ANNUAL_SALARY_INCREASE
    )
    assert calculated_value == expected_value


def test_expected_retirement_savings_calculation_matches_expected_value(
    mock_calculation_data: dict,
):
    # Manually calculated value using values from mock_calculation_data
    expected_value = 1_347_347
    user = User.model_validate(mock_calculation_data)
    calculated_value = user.calculate_expected_savings_at_retirement(
        annual_salary_increase=ANNUAL_SALARY_INCREASE
    )
    assert calculated_value == expected_value


def test_required_retirement_savings_calculation_matches_expected_value(
    mock_calculation_data: dict,
):
    # Manually calculated value using values from mock_calculation_data
    expected_value = 903_589
    user = User.model_validate(mock_calculation_data)
    calculated_value = user.calculate_required_retirement_savings(
        inflation_rate=INFLATION_RATE, annual_salary_increase=ANNUAL_SALARY_INCREASE
    )
    assert calculated_value == expected_value
