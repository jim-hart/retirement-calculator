import click

from retirement_calculator.client import get_user_data


@click.command()
@click.argument("user_id", type=int)
@click.option(
    "-r",
    "--annual-salary-increase",
    type=float,
    default=0.02,
    show_default=True,
    help="The annual expected salary increase for the target user",
)
@click.option(
    "-i",
    "--inflation-rate",
    type=float,
    default=0.03,
    show_default=True,
    help="The inflation rate used to calculate the purchasing power of future savings",
)
def main(user_id: int, annual_salary_increase: float, inflation_rate: float) -> None:
    """
    :param      user_id:                    The ID of the target user.
    :param      annual_salary_increase:  The expected increase (as a percentage) <user>
                                         can expect each year. increase each year.
    :param      inflation_rate:          The inflation rate to account for in
                                         pre-and-post-retirement.
    """
    user = get_user_data(user_id)
    required_retirement_savings = user.calculate_required_retirement_savings(
        annual_salary_increase=annual_salary_increase, inflation_rate=inflation_rate
    )
    expected_retirement_savings = user.calculate_expected_savings_at_retirement(
        annual_salary_increase=annual_salary_increase
    )

    click.echo(f"\nTo retire at age {user.retirement_age}")
    click.echo(f"You will need:       ${required_retirement_savings:>10,}")
    click.echo(f"You will have saved: ${expected_retirement_savings:>10,}\n")


if __name__ == "__main__":
    main()
