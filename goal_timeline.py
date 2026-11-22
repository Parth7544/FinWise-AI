
import math


def calculate_goal_timeline(goal_amount, current_savings, monthly_savings):

    try:
        goal_amount = float(goal_amount)
        current_savings = float(current_savings)
        monthly_savings = float(monthly_savings)
    except (TypeError, ValueError):
        return {
            "months_required": 0,
            "status": "Invalid Input"
        }

    if not all(math.isfinite(value) for value in [
        goal_amount, current_savings, monthly_savings
    ]):
        return {
            "months_required": 0,
            "status": "Invalid Input"
        }

    if goal_amount <= 0 or current_savings < 0 or monthly_savings <= 0:
        return {
            "months_required": 0,
            "status": "Invalid Input"
        }

    remaining_amount = max(goal_amount - current_savings, 0)

    if remaining_amount == 0:
        return {
            "months_required": 0,
            "status": "Goal Already Achieved"
        }

    months_required = math.ceil(
        remaining_amount / monthly_savings
    )

    return {
        "months_required": months_required,
        "status": "Goal In Progress"
    }
