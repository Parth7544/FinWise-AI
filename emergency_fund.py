
import math


def analyze_emergency_fund(monthly_expenses, current_fund):

    try:
        monthly_expenses = float(monthly_expenses)
        current_fund = float(current_fund)

    except (TypeError, ValueError):
        return {
            "months_covered": 0,
            "minimum_target": 0,
            "recommended_target": 0,
            "status": "Invalid Input"
        }

    if not all(math.isfinite(value) for value in [
        monthly_expenses, current_fund
    ]):
        return {
            "months_covered": 0,
            "minimum_target": 0,
            "recommended_target": 0,
            "status": "Invalid Input"
        }

    if monthly_expenses <= 0 or current_fund < 0:
        return {
            "months_covered": 0,
            "minimum_target": 0,
            "recommended_target": 0,
            "status": "Invalid Input"
        }

    try:
        months_covered = current_fund / monthly_expenses

        minimum_target = monthly_expenses * 3
        recommended_target = monthly_expenses * 6

    except (OverflowError, ZeroDivisionError):
        return {
            "months_covered": 0,
            "minimum_target": 0,
            "recommended_target": 0,
            "status": "Invalid Input"
        }

    if not all(math.isfinite(value) for value in [
        months_covered, minimum_target, recommended_target
    ]):
        return {
            "months_covered": 0,
            "minimum_target": 0,
            "recommended_target": 0,
            "status": "Invalid Input"
        }

    if months_covered >= 6:
        status = "Excellent"
    elif months_covered >= 3:
        status = "Good"
    else:
        status = "Needs Improvement"

    return {
        "months_covered": round(months_covered, 2),
        "minimum_target": round(minimum_target, 2),
        "recommended_target": round(recommended_target, 2),
        "status": status
    }
