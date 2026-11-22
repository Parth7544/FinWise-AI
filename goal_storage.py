
import pandas as pd
import os
import math

GOALS_FILE = "data/financial_goals.csv"


def save_goals(goals):

    columns = ["name", "target", "saved"]

    if not isinstance(goals, list):
        return False

    validated_goals = []

    for goal in goals:

        if not isinstance(goal, dict):
            return False

        if not all(key in goal for key in columns):
            return False

        if not isinstance(goal["name"], str) or not goal["name"].strip():
            return False

        try:
            target = float(goal["target"])
            saved = float(goal["saved"])
        except (TypeError, ValueError):
            return False

        if not all(math.isfinite(value) for value in [target, saved]):
            return False

        if target <= 0 or saved < 0:
            return False

        validated_goals.append({
            "name": goal["name"].strip(),
            "target": target,
            "saved": saved
        })

    df = pd.DataFrame(validated_goals, columns=columns)

    os.makedirs(os.path.dirname(GOALS_FILE), exist_ok=True)

    df.to_csv(GOALS_FILE, index=False)

    return True


def load_goals():

    if not os.path.exists(GOALS_FILE):
        return []

    try:
        df = pd.read_csv(GOALS_FILE)
    except pd.errors.EmptyDataError:
        return []

    columns = ["name", "target", "saved"]

    if not all(column in df.columns for column in columns):
        return []

    return df[columns].to_dict(orient="records")
