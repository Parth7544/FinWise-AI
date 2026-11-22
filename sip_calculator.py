
import math


def calculate_sip(monthly_investment, annual_return_rate, years):

    try:
        monthly_investment = float(monthly_investment)
        annual_return_rate = float(annual_return_rate)
        years = float(years)

    except (TypeError, ValueError):
        return {
            "total_invested": 0,
            "maturity_value": 0,
            "wealth_gained": 0,
            "status": "Invalid Input"
        }

    if not all(math.isfinite(value) for value in [
        monthly_investment, annual_return_rate, years
    ]):
        return {
            "total_invested": 0,
            "maturity_value": 0,
            "wealth_gained": 0,
            "status": "Invalid Input"
        }

    if monthly_investment <= 0 or annual_return_rate < 0 or years <= 0:
        return {
            "total_invested": 0,
            "maturity_value": 0,
            "wealth_gained": 0,
            "status": "Invalid Input"
        }

    months = years * 12
    monthly_rate = annual_return_rate / 100 / 12

    total_invested = monthly_investment * months

    if monthly_rate == 0:
        maturity_value = total_invested
    else:
        maturity_value = (
            monthly_investment
            * (((1 + monthly_rate) ** months - 1) / monthly_rate)
            * (1 + monthly_rate)
        )

    wealth_gained = maturity_value - total_invested

    return {
        "total_invested": round(total_invested, 2),
        "maturity_value": round(maturity_value, 2),
        "wealth_gained": round(wealth_gained, 2),
        "status": "SIP Calculation Successful"
    }
