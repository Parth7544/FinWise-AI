
import math


def calculate_goal_milestones(goal_amount, current_savings):

    try:
        goal_amount = float(goal_amount)
        current_savings = float(current_savings)
    except (TypeError, ValueError):
        return []

    if not all(math.isfinite(value) for value in [goal_amount, current_savings]):
        return []

    if goal_amount <= 0 or current_savings < 0:
        return []

    milestones = [25, 50, 75, 100]

    results = []

    for milestone in milestones:

        required_amount = goal_amount * milestone / 100

        results.append({
            "milestone": milestone,
            "required_amount": required_amount,
            "achieved": current_savings >= required_amount
        })

    return results
