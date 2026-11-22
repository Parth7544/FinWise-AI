
import math


def analyze_savings_rate(income, savings):

    try:
        income = float(income)
        savings = float(savings)

    except (TypeError, ValueError):
        return {
            "savings_rate": 0,
            "rating": "Invalid Input",
            "recommendation": "Enter valid financial information."
        }

    if not all(math.isfinite(value) for value in [
        income, savings
    ]):
        return {
            "savings_rate": 0,
            "rating": "Invalid Input",
            "recommendation": "Enter valid financial information."
        }

    if income <= 0 or savings < 0:
        return {
            "savings_rate": 0,
            "rating": "Invalid Input",
            "recommendation": "Enter valid financial information."
        }

    try:
        savings_rate = (savings / income) * 100

    except (OverflowError, ZeroDivisionError):
        return {
            "savings_rate": 0,
            "rating": "Invalid Input",
            "recommendation": "Enter valid financial information."
        }

    if not math.isfinite(savings_rate):
        return {
            "savings_rate": 0,
            "rating": "Invalid Input",
            "recommendation": "Enter valid financial information."
        }

    if savings_rate >= 30:
        rating = "Excellent"
        recommendation = "Excellent savings habit. Maintain consistency."

    elif savings_rate >= 20:
        rating = "Good"
        recommendation = "Good savings performance. Try increasing it gradually."

    elif savings_rate >= 10:
        rating = "Average"
        recommendation = "Try reducing unnecessary expenses to save more."

    else:
        rating = "Poor"
        recommendation = "Create a budget and prioritize regular savings."

    return {
        "savings_rate": round(savings_rate, 2),
        "rating": rating,
        "recommendation": recommendation
    }
