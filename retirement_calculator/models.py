from datetime import date
from typing import Self, NamedTuple

from pydantic import BaseModel, field_validator, model_validator


class UserFinancials(NamedTuple):
    """
    A simple container for encapsulating data about a User's financial situation so that
    consumers can pass around that data while making use of type checkers.
    """

    expected_retirement_savings: int
    required_retirement_savings: int


class User(BaseModel):
    id: int
    address: str
    full_name: str

    date_of_birth: date
    life_expectancy: int
    retirement_age: int

    current_retirement_savings: int
    household_income: int

    current_savings_rate: float
    expected_rate_of_return: float
    pre_retirement_income_percent: float

    @field_validator(
        "current_savings_rate",
        "expected_rate_of_return",
        "pre_retirement_income_percent",
        mode="before",
    )
    @classmethod
    def convert_written_percentage_to_numeric_form(cls, v: int) -> float:
        """
        :returns:   A percentage value in written notation converted to its
                    numerical form (e.g. 9% -> 0.09).
        """
        return v / 100

    @model_validator(mode="after")
    def check_retirement_age_is_greater_than_current_age(self) -> Self:
        if self.retirement_age <= self.current_age:
            raise ValueError("Retirement age must be greater than current age")
        return self

    @model_validator(mode="after")
    def check_life_expectancy_greater_than_retirement_age(self) -> Self:
        if self.life_expectancy <= self.retirement_age:
            raise ValueError("Life expectancy must be greater than retirement age")
        return self

    @property
    def current_age(self) -> int:
        """
        :returns:   This User's current approximate age in years, rounded down.
        """
        delta = date.today() - self.date_of_birth
        return int(delta.days / 365.25)

    @property
    def years_to_retirement(self) -> int:
        return self.retirement_age - self.current_age

    @property
    def expected_years_in_retirement(self) -> int:
        return self.life_expectancy - self.retirement_age

    def calculate_required_retirement_income(
        self, annual_salary_increase: float
    ) -> int:
        """
        :param      annual_salary_increase: The expected percentage this User's salary
                                            will increase each year.

        :returns:   The yearly expenses of this User when they retire based off their
                    projected future income.
        """
        r = annual_salary_increase
        t = self.years_to_retirement
        P = self.household_income

        #                t
        # A = P × (1 + r)
        future_salary = P * (1 + r) ** t
        return round(future_salary * self.pre_retirement_income_percent)

    def calculate_expected_savings_at_retirement(
        self, annual_salary_increase: float
    ) -> int:
        """
        :param      annual_salary_increase: The expected percentage this User's salary
                                            will increase each year.

        :returns:   The expected savings for this User at retirement using (in
                    part) the formula for calculating the future value of a
                    growing annuity.

                    # The formula used to calculate this is as follows:
                    #
                    #                           ⎛       t          t⎞
                    #                 t         ⎜(1 + r)  - (1 + g) ⎟
                    # FV = P × (1 + r)  + PMT × ⎜───────────────────⎟
                    #                           ⎝       r - g       ⎠
                    #
        """
        t = self.years_to_retirement
        r = self.expected_rate_of_return
        g = annual_salary_increase
        P = self.current_retirement_savings
        PMT = self.household_income * self.current_savings_rate

        #            t
        # P × (1 + r)
        compounded_initial_lump_sum = P * ((1 + r) ** t)

        #       ⎛       t          t⎞
        #       ⎜(1 + r)  - (1 + g) ⎟
        # PMT × ⎜───────────────────⎟
        #       ⎝       r - g       ⎠
        future_value_growth_annuity = PMT * (((1 + r) ** t - (1 + g) ** t) / (r - g))

        # P + PMT
        return round(compounded_initial_lump_sum + future_value_growth_annuity)

    def calculate_required_retirement_savings(
        self, inflation_rate: float, annual_salary_increase: float
    ) -> int:
        """
        :param      inflation_rate: The inflation rate to take into account
                                    when calculating the required savings this User will
                                    need to retire.
        :param      annual_salary_increase: The expected percentage this User's salary
                                            will increase each year.

        :returns:   The total savings required for this User to retire at
                    their target age taking into account the effects inflation and
                    annual salary increases.

                    # The formula used to calculate this is as follows:
                    #
                    #
                    #          ⎛    ⎛             -t⎞ ⎞
                    #          ⎜1 - ⎝(1 + (r - i))  ⎠ ⎟
                    # FV = A × ⎜─────────────────────⎟
                    #          ⎝        r - i        ⎠
                    #

        """
        i = inflation_rate
        r = self.expected_rate_of_return
        t = self.expected_years_in_retirement
        A = self.calculate_required_retirement_income(annual_salary_increase)

        required_savings = A * ((1 - ((1 + (r - i)) ** -t)) / (r - i))
        return round(required_savings)
