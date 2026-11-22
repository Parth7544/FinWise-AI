
import math


def calculate_fd(principal, annual_interest_rate, years):

    try:
        principal = float(principal)
        annual_interest_rate = float(annual_interest_rate)
        years = float(years)

    except (TypeError, ValueError):
        return {
            "maturity_amount": 0,
            "total_interest": 0,
            "status": "Invalid Input"
        }

    if not all(math.isfinite(value) for value in [
        principal, annual_interest_rate, years
    ]):
        return {
            "maturity_amount": 0,
            "total_interest": 0,
            "status": "Invalid Input"
        }

    if principal <= 0 or annual_interest_rate < 0 or years <= 0:
        return {
            "maturity_amount": 0,
            "total_interest": 0,
            "status": "Invalid Input"
        }

    maturity_amount = principal * (
        1 + annual_interest_rate / 100 / 4
    ) ** (4 * years)

    total_interest = maturity_amount - principal

    return {
        "maturity_amount": round(maturity_amount, 2),
        "total_interest": round(total_interest, 2),
        "status": "FD Calculation Successful"
    }
