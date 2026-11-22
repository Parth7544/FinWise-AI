
import pandas as pd
import math


def forecast_monthly_expenses(df):

    columns = ["Category", "Predicted Expenses"]

    if not isinstance(df, pd.DataFrame):
        return pd.DataFrame(columns=columns)

    required_columns = ["Date", "Type", "Category", "Amount"]

    if not all(column in df.columns for column in required_columns):
        return pd.DataFrame(columns=columns)

    if df.empty:
        return pd.DataFrame(columns=columns)

    expense_df = df[df["Type"] == "Expense"].copy()

    if expense_df.empty:
        return pd.DataFrame(columns=columns)

    try:
        expense_df["Date"] = pd.to_datetime(
            expense_df["Date"], errors="raise"
        )

        expense_df["Amount"] = pd.to_numeric(
            expense_df["Amount"], errors="raise"
        )

    except (TypeError, ValueError):
        return pd.DataFrame(columns=columns)

    if expense_df["Date"].isna().any():
        return pd.DataFrame(columns=columns)

    if not all(
        math.isfinite(value) and value >= 0
        for value in expense_df["Amount"]
    ):
        return pd.DataFrame(columns=columns)

    if expense_df["Category"].isna().any():
        return pd.DataFrame(columns=columns)

    if not expense_df["Category"].apply(
        lambda value: isinstance(value, str) and bool(value.strip())
    ).all():
        return pd.DataFrame(columns=columns)

    expense_df["Month"] = (
        expense_df["Date"].dt.to_period("M").astype(str)
    )

    monthly_expenses = expense_df.groupby(
        ["Month", "Category"]
    )["Amount"].sum().reset_index()

    forecast = monthly_expenses.groupby(
        "Category"
    )["Amount"].mean().reset_index()

    forecast.rename(
        columns={"Amount": "Predicted Expenses"},
        inplace=True
    )

    forecast["Predicted Expenses"] = (
        forecast["Predicted Expenses"].round(2)
    )

    return forecast[columns]
