
import math


def calculate_loan_emi(principal, annual_interest_rate, years):

    try:
        principal = float(principal)
        annual_interest_rate = float(annual_interest_rate)
        years = float(years)

    except (TypeError, ValueError):
        return {
            "monthly_emi": 0,
            "total_payment": 0,
            "total_interest": 0,
            "status": "Invalid Input"
        }

    if not all(math.isfinite(value) for value in [
        principal, annual_interest_rate, years
    ]):
        return {
            "monthly_emi": 0,
            "total_payment": 0,
            "total_interest": 0,
            "status": "Invalid Input"
        }

    if principal <= 0 or annual_interest_rate < 0 or years <= 0:
        return {
            "monthly_emi": 0,
            "total_payment": 0,
            "total_interest": 0,
            "status": "Invalid Input"
        }

    months = years * 12
    monthly_rate = annual_interest_rate / 12 / 100

    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = (
            principal * monthly_rate *
            (1 + monthly_rate) ** months
        ) / (
            (1 + monthly_rate) ** months - 1
        )

    total_payment = emi * months
    total_interest = total_payment - principal

    return {
        "monthly_emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
        "status": "EMI Calculated Successfully"
    }
