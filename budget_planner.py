
import pandas as pd
import math


def create_budget_analysis(df, monthly_budget):

    columns = [
        "Category",
        "Budget",
        "Actual Spending",
        "Remaining",
        "Status"
    ]

    if not isinstance(df, pd.DataFrame):
        return pd.DataFrame(columns=columns)

    if not isinstance(monthly_budget, dict):
        return pd.DataFrame(columns=columns)

    required_columns = ["Type", "Category", "Amount"]

    if not all(column in df.columns for column in required_columns):
        return pd.DataFrame(columns=columns)

    validated_budgets = {}

    for category, budget in monthly_budget.items():

        if not isinstance(category, str) or not category.strip():
            return pd.DataFrame(columns=columns)

        try:
            budget = float(budget)
        except (TypeError, ValueError):
            return pd.DataFrame(columns=columns)

        if not math.isfinite(budget) or budget < 0:
            return pd.DataFrame(columns=columns)

        validated_budgets[category] = budget

    expense_df = df[df["Type"] == "Expense"].copy()

    try:
        expense_df["Amount"] = pd.to_numeric(
            expense_df["Amount"], errors="raise"
        )
    except (TypeError, ValueError):
        return pd.DataFrame(columns=columns)

    if not all(math.isfinite(value) and value >= 0
               for value in expense_df["Amount"]):
        return pd.DataFrame(columns=columns)

    actual_expenses = expense_df.groupby("Category")["Amount"].sum()

    budget_data = []

    for category, budget in validated_budgets.items():

        actual = actual_expenses.get(category, 0)
        remaining = budget - actual

        status = "Over Budget" if remaining < 0 else "Within Budget"

        budget_data.append({
            "Category": category,
            "Budget": budget,
            "Actual Spending": actual,
            "Remaining": remaining,
            "Status": status
        })

    return pd.DataFrame(budget_data, columns=columns)
