from datetime import date, timedelta

import pytest


@pytest.fixture
def mock_user_data() -> dict:
    """
    :returns:   Static user data that can be used to instantiate an instance of "User".
    """

    # always return someone ≈ 30 years old, so we can use a static time frame
    date_of_birth = date.today() - timedelta(days=(365 * 30) + 10)
    return {
        "id": 1,
        "address": "26 Piazza di Spagna\nRome, Italy 00187",
        "full_name": "John Keats",
        "date_of_birth": date_of_birth.isoformat(),
        "life_expectancy": 90,
        "retirement_age": 60,
        "current_retirement_savings": 10_000,
        "household_income": 60_000,
        "current_savings_rate": 10,
        "expected_rate_of_return": 10,
        "pre_retirement_income_percent": 67,
    }
