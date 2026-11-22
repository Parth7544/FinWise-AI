
import math


def analyze_financial_risk(income, expenses, savings):

    try:
        income = float(income)
        expenses = float(expenses)
        savings = float(savings)

    except (TypeError, ValueError):
        return {
            "risk_level": "Unknown",
            "expense_ratio": 0,
            "savings_ratio": 0,
            "recommendations": ["Enter valid financial information."]
        }

    if not all(math.isfinite(value) for value in [
        income, expenses, savings
    ]):
        return {
            "risk_level": "Unknown",
            "expense_ratio": 0,
            "savings_ratio": 0,
            "recommendations": ["Enter valid financial information."]
        }

    if income <= 0 or expenses < 0 or savings < 0:
        return {
            "risk_level": "Unknown",
            "expense_ratio": 0,
            "savings_ratio": 0,
            "recommendations": ["Enter valid financial information."]
        }

    try:
        expense_ratio = (expenses / income) * 100
        savings_ratio = (savings / income) * 100

    except (OverflowError, ZeroDivisionError):
        return {
            "risk_level": "Unknown",
            "expense_ratio": 0,
            "savings_ratio": 0,
            "recommendations": ["Enter valid financial information."]
        }

    if not all(math.isfinite(value) for value in [
        expense_ratio, savings_ratio
    ]):
        return {
            "risk_level": "Unknown",
            "expense_ratio": 0,
            "savings_ratio": 0,
            "recommendations": ["Enter valid financial information."]
        }

    recommendations = []

    if expense_ratio > 80:
        risk_level = "High"
        recommendations.append(
            "Expenses are very high compared with income."
        )

    elif expense_ratio > 60:
        risk_level = "Moderate"
        recommendations.append(
            "Review expenses and reduce unnecessary spending."
        )

    else:
        risk_level = "Low"
        recommendations.append(
            "Your current expense-to-income ratio is healthy."
        )

    if savings_ratio < 10:
        recommendations.append(
            "Try to increase your monthly savings."
        )

    if savings < 0:
        recommendations.append(
            "Your expenses exceed your income. Review your budget immediately."
        )

    return {
        "risk_level": risk_level,
        "expense_ratio": round(expense_ratio, 2),
        "savings_ratio": round(savings_ratio, 2),
        "recommendations": recommendations
    }
