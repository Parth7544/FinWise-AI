
import math


def calculate_rd(monthly_deposit, annual_interest_rate, years):

    try:
        monthly_deposit = float(monthly_deposit)
        annual_interest_rate = float(annual_interest_rate)
        years = float(years)

    except (TypeError, ValueError):
        return {
            "total_invested": 0,
            "maturity_amount": 0,
            "total_interest": 0,
            "status": "Invalid Input"
        }

    if not all(math.isfinite(value) for value in [
        monthly_deposit, annual_interest_rate, years
    ]):
        return {
            "total_invested": 0,
            "maturity_amount": 0,
            "total_interest": 0,
            "status": "Invalid Input"
        }

    if monthly_deposit <= 0 or annual_interest_rate < 0 or years <= 0:
        return {
            "total_invested": 0,
            "maturity_amount": 0,
            "total_interest": 0,
            "status": "Invalid Input"
        }

    if not years.is_integer():
        return {
            "total_invested": 0,
            "maturity_amount": 0,
            "total_interest": 0,
            "status": "Invalid Input"
        }

    quarters = int(years * 4)
    total_invested = monthly_deposit * years * 12

    balance = 0

    quarterly_rate = annual_interest_rate / 100 / 4
    monthly_rate = annual_interest_rate / 100 / 12

    for quarter in range(quarters):

        interest = balance * quarterly_rate

        interest += monthly_deposit * monthly_rate * (3 + 2 + 1)

        balance += (monthly_deposit * 3) + interest

    maturity_amount = balance
    total_interest = maturity_amount - total_invested

    return {
        "total_invested": round(total_invested, 2),
        "maturity_amount": round(maturity_amount, 2),
        "total_interest": round(total_interest, 2),
        "status": "RD Calculation Successful"
    }
