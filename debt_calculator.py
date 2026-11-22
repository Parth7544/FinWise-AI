
import math


def calculate_debt_repayment(
    debt_amount,
    monthly_payment,
    annual_interest_rate
):

    try:
        debt_amount = float(debt_amount)
        monthly_payment = float(monthly_payment)
        annual_interest_rate = float(annual_interest_rate)

    except (TypeError, ValueError):
        return {
            "months_required": 0,
            "total_payment": 0,
            "total_interest": 0,
            "status": "Invalid Input"
        }

    if not all(math.isfinite(value) for value in [
        debt_amount, monthly_payment, annual_interest_rate
    ]):
        return {
            "months_required": 0,
            "total_payment": 0,
            "total_interest": 0,
            "status": "Invalid Input"
        }

    if debt_amount <= 0 or monthly_payment <= 0 or annual_interest_rate < 0:
        return {
            "months_required": 0,
            "total_payment": 0,
            "total_interest": 0,
            "status": "Invalid Input"
        }

    monthly_rate = annual_interest_rate / 100 / 12

    if monthly_rate > 0:
        monthly_interest = debt_amount * monthly_rate

        if monthly_payment <= monthly_interest:
            return {
                "months_required": 0,
                "total_payment": 0,
                "total_interest": 0,
                "status": "Monthly payment is too low to repay the debt."
            }

    balance = debt_amount
    total_payment = 0
    months = 0

    while balance > 0 and months < 1200:

        interest = balance * monthly_rate
        payment = min(monthly_payment, balance + interest)

        balance = balance + interest - payment

        total_payment += payment
        months += 1

    if balance > 0:
        return {
            "months_required": months,
            "total_payment": round(total_payment, 2),
            "total_interest": round(total_payment - debt_amount, 2),
            "status": "Repayment period exceeds the calculation limit."
        }

    return {
        "months_required": months,
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_payment - debt_amount, 2),
        "status": "Debt Repayment Plan Calculated"
    }
