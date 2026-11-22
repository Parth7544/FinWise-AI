
import math


def calculate_investment_return(
    principal,
    annual_return_rate,
    years
):

    try:
        principal = float(principal)
        annual_return_rate = float(annual_return_rate)
        years = float(years)

    except (TypeError, ValueError):
        return {
            "final_value": 0,
            "total_profit": 0,
            "status": "Invalid Input"
        }

    if not all(math.isfinite(value) for value in [
        principal, annual_return_rate, years
    ]):
        return {
            "final_value": 0,
            "total_profit": 0,
            "status": "Invalid Input"
        }

    if principal <= 0 or annual_return_rate < 0 or years <= 0:
        return {
            "final_value": 0,
            "total_profit": 0,
            "status": "Invalid Input"
        }

    try:
        final_value = principal * (
            1 + annual_return_rate / 100
        ) ** years

        total_profit = final_value - principal

    except (OverflowError, ValueError):
        return {
            "final_value": 0,
            "total_profit": 0,
            "status": "Invalid Input"
        }

    if not math.isfinite(final_value):
        return {
            "final_value": 0,
            "total_profit": 0,
            "status": "Invalid Input"
        }

    return {
        "final_value": round(final_value, 2),
        "total_profit": round(total_profit, 2),
        "status": "Investment Calculation Successful"
    }
