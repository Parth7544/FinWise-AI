
import math
import pandas as pd


def calculate_financial_health(income, expenses, savings, budget_result):

    try:
        income = float(income)
        expenses = float(expenses)
        savings = float(savings)

    except (TypeError, ValueError):
        return {
            "score": 0,
            "rating": "Invalid Input",
            "savings_rate": 0,
            "budget_score": 0
        }

    if not all(math.isfinite(value) for value in [
        income, expenses, savings
    ]):
        return {
            "score": 0,
            "rating": "Invalid Input",
            "savings_rate": 0,
            "budget_score": 0
        }

    if income <= 0 or expenses < 0 or savings < 0:
        return {
            "score": 0,
            "rating": "Invalid Input",
            "savings_rate": 0,
            "budget_score": 0
        }

    if budget_result is not None:
        if not isinstance(budget_result, pd.DataFrame):
            return {
                "score": 0,
                "rating": "Invalid Input",
                "savings_rate": 0,
                "budget_score": 0
            }

        if not budget_result.empty and "Status" not in budget_result.columns:
            return {
                "score": 0,
                "rating": "Invalid Input",
                "savings_rate": 0,
                "budget_score": 0
            }

    try:
        savings_rate = (savings / income) * 100

        # Savings score: maximum 40 points
        savings_score = min(max(savings_rate, 0) / 20 * 40, 40)

        # Budget score: maximum 30 points
        if budget_result is not None and not budget_result.empty:
            within_budget = (
                budget_result["Status"] == "Within Budget"
            ).sum()

            budget_score = (
                within_budget / len(budget_result)
            ) * 30
        else:
            budget_score = 0

        # Expense management score: maximum 30 points
        expense_ratio = (expenses / income) * 100
        expense_score = max(0, 30 - (expense_ratio / 100 * 30))

        total_score = round(
            savings_score + budget_score + expense_score
        )

    except (TypeError, ValueError, OverflowError, ZeroDivisionError):
        return {
            "score": 0,
            "rating": "Invalid Input",
            "savings_rate": 0,
            "budget_score": 0
        }

    if not all(math.isfinite(value) for value in [
        savings_rate, budget_score, expense_score, total_score
    ]):
        return {
            "score": 0,
            "rating": "Invalid Input",
            "savings_rate": 0,
            "budget_score": 0
        }

    if total_score >= 80:
        rating = "Excellent"
    elif total_score >= 60:
        rating = "Good"
    elif total_score >= 40:
        rating = "Average"
    else:
        rating = "Needs Improvement"

    return {
        "score": total_score,
        "rating": rating,
        "savings_rate": round(savings_rate, 2),
        "budget_score": round(float(budget_score), 2)
    }
