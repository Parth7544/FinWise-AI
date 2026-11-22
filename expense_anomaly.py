
import pandas as pd
import math


def detect_expense_anomalies(df):

    columns = ["Date", "Category", "Amount", "mean"]

    if not isinstance(df, pd.DataFrame):
        return pd.DataFrame(columns=columns)

    required_columns = ["Date", "Type", "Category", "Amount"]

    if not all(column in df.columns for column in required_columns):
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

    category_stats = expense_df.groupby("Category")["Amount"].agg(
        ["mean", "std"]
    ).reset_index()

    expense_df = expense_df.merge(
        category_stats,
        on="Category",
        how="left"
    )

    expense_df["Is Anomaly"] = (
        expense_df["Amount"] >
        expense_df["mean"] + 1.5 * expense_df["std"].fillna(0)
    )

    anomalies = expense_df[
        expense_df["Is Anomaly"]
    ].copy()

    return anomalies[columns]
