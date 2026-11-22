
import pandas as pd
import math


def detect_recurring_expenses(df):

    columns = [
        "Description",
        "Category",
        "Occurrences",
        "Average_Amount",
        "Total_Amount"
    ]

    if not isinstance(df, pd.DataFrame):
        return pd.DataFrame(columns=columns)

    required_columns = [
        "Type",
        "Description",
        "Category",
        "Amount"
    ]

    if not all(column in df.columns for column in required_columns):
        return pd.DataFrame(columns=columns)

    expense_df = df[
        df["Type"] == "Expense"
    ].copy()

    if expense_df.empty:
        return pd.DataFrame(columns=columns)

    try:
        expense_df["Amount"] = pd.to_numeric(
            expense_df["Amount"], errors="raise"
        )
    except (TypeError, ValueError):
        return pd.DataFrame(columns=columns)

    if not all(
        math.isfinite(value) and value >= 0
        for value in expense_df["Amount"]
    ):
        return pd.DataFrame(columns=columns)

    for column in ["Description", "Category"]:

        if expense_df[column].isna().any():
            return pd.DataFrame(columns=columns)

        if not expense_df[column].apply(
            lambda value: isinstance(value, str) and bool(value.strip())
        ).all():
            return pd.DataFrame(columns=columns)

    recurring = (
        expense_df.groupby(["Description", "Category"])
        .agg(
            Occurrences=("Amount", "count"),
            Average_Amount=("Amount", "mean"),
            Total_Amount=("Amount", "sum")
        )
        .reset_index()
    )

    recurring = recurring[
        recurring["Occurrences"] >= 2
    ].copy()

    recurring["Average_Amount"] = (
        recurring["Average_Amount"].round(2)
    )

    return recurring[columns]
