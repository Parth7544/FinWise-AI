
import math


def analyze_spending_behavior(income, expenses):

    try:
        income = float(income)
        expenses = float(expenses)
    except (TypeError, ValueError):
        return {
            "expense_ratio": 0,
            "behavior": "Invalid Input",
            "recommendation": "Enter valid financial information."
        }

    if not all(math.isfinite(value) for value in [income, expenses]):
        return {
            "expense_ratio": 0,
            "behavior": "Invalid Input",
            "recommendation": "Enter valid financial information."
        }

    if income <= 0 or expenses < 0:
        return {
            "expense_ratio": 0,
            "behavior": "Invalid Input",
            "recommendation": "Enter valid financial information."
        }

    expense_ratio = (expenses / income) * 100

    if not math.isfinite(expense_ratio):
        return {
            "expense_ratio": 0,
            "behavior": "Invalid Input",
            "recommendation": "Enter valid financial information."
        }

    if expense_ratio <= 50:
        behavior = "Low Spending"
        recommendation = "Good spending control. Continue saving regularly."

    elif expense_ratio <= 75:
        behavior = "Moderate Spending"
        recommendation = "Review discretionary expenses and increase savings."

    else:
        behavior = "High Spending"
        recommendation = "Reduce unnecessary expenses and create a stricter budget."

    return {
        "expense_ratio": round(expense_ratio, 2),
        "behavior": behavior,
        "recommendation": recommendation
    }
