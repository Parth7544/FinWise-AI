
import math


def calculate_monthly_savings(goal_amount, current_savings, months):

    try:
        goal_amount = float(goal_amount)
        current_savings = float(current_savings)
        months = float(months)
    except (TypeError, ValueError):
        return {
            "monthly_savings": 0,
            "remaining_amount": 0,
            "status": "Invalid Input"
        }

    if not all(math.isfinite(value) for value in [
        goal_amount, current_savings, months
    ]):
        return {
            "monthly_savings": 0,
            "remaining_amount": 0,
            "status": "Invalid Input"
        }

    if goal_amount <= 0 or current_savings < 0 or months <= 0:
        return {
            "monthly_savings": 0,
            "remaining_amount": 0,
            "status": "Invalid Input"
        }

    remaining_amount = max(goal_amount - current_savings, 0)

    monthly_savings = remaining_amount / months

    status = (
        "Goal Already Achieved"
        if remaining_amount == 0
        else "Monthly Plan Created"
    )

    return {
        "monthly_savings": round(monthly_savings, 2),
        "remaining_amount": round(remaining_amount, 2),
        "status": status
    }
