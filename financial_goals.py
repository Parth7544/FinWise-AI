
import math


def calculate_goal_progress(goal_amount, current_savings):

    try:
        goal_amount = float(goal_amount)
        current_savings = float(current_savings)
    except (TypeError, ValueError):
        return {
            "progress": 0,
            "remaining": 0,
            "status": "Invalid Input"
        }

    if not all(math.isfinite(value) for value in [goal_amount, current_savings]):
        return {
            "progress": 0,
            "remaining": 0,
            "status": "Invalid Input"
        }

    if goal_amount <= 0 or current_savings < 0:
        return {
            "progress": 0,
            "remaining": 0,
            "status": "Invalid Input"
        }

    progress = min((current_savings / goal_amount) * 100, 100)
    remaining = max(goal_amount - current_savings, 0)

    status = "Goal Achieved" if current_savings >= goal_amount else "In Progress"

    return {
        "progress": round(progress, 2),
        "remaining": round(remaining, 2),
        "status": status
    }
