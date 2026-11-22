
import math


def analyze_goal_priority(goals):

    if not goals:
        return {
            "priority_goal": None,
            "reason": "No savings goals available."
        }

    if not isinstance(goals, list):
        return {
            "priority_goal": None,
            "reason": "Invalid Goal Data."
        }

    validated_goals = []

    for goal in goals:

        if not isinstance(goal, dict):
            return {
                "priority_goal": None,
                "reason": "Invalid Goal Data."
            }

        if not all(key in goal for key in ["name", "saved", "target"]):
            return {
                "priority_goal": None,
                "reason": "Invalid Goal Data."
            }

        if not isinstance(goal["name"], str) or not goal["name"].strip():
            return {
                "priority_goal": None,
                "reason": "Invalid Goal Data."
            }

        try:
            saved = float(goal["saved"])
            target = float(goal["target"])
        except (TypeError, ValueError):
            return {
                "priority_goal": None,
                "reason": "Invalid Goal Data."
            }

        if not all(math.isfinite(value) for value in [saved, target]):
            return {
                "priority_goal": None,
                "reason": "Invalid Goal Data."
            }

        if saved < 0 or target <= 0:
            return {
                "priority_goal": None,
                "reason": "Invalid Goal Data."
            }

        validated_goals.append({
            "name": goal["name"],
            "saved": saved,
            "target": target
        })

    incomplete_goals = [
        goal for goal in validated_goals
        if goal["saved"] < goal["target"]
    ]

    if not incomplete_goals:
        return {
            "priority_goal": None,
            "reason": "All savings goals have been achieved!"
        }

    priority_goal = min(
        incomplete_goals,
        key=lambda goal: goal["saved"] / goal["target"]
    )

    progress = (
        priority_goal["saved"] / priority_goal["target"]
    ) * 100

    return {
        "priority_goal": priority_goal["name"],
        "progress": round(progress, 2),
        "remaining": round(
            priority_goal["target"] - priority_goal["saved"], 2
        ),
        "reason": "This goal has the lowest completion percentage."
    }
