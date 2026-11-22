
import math


def calculate_net_worth(
    cash,
    savings,
    investments,
    property,
    other_assets,
    loans,
    credit_card_debt,
    other_liabilities
):

    assets = [
        cash,
        savings,
        investments,
        property,
        other_assets
    ]

    liabilities = [
        loans,
        credit_card_debt,
        other_liabilities
    ]

    try:
        assets = [float(value) for value in assets]
        liabilities = [float(value) for value in liabilities]

    except (TypeError, ValueError):
        return {
            "total_assets": 0,
            "total_liabilities": 0,
            "net_worth": 0,
            "status": "Invalid Input"
        }

    all_values = assets + liabilities

    if not all(math.isfinite(value) for value in all_values):
        return {
            "total_assets": 0,
            "total_liabilities": 0,
            "net_worth": 0,
            "status": "Invalid Input"
        }

    if any(value < 0 for value in all_values):
        return {
            "total_assets": 0,
            "total_liabilities": 0,
            "net_worth": 0,
            "status": "Invalid Input"
        }

    total_assets = sum(assets)
    total_liabilities = sum(liabilities)

    net_worth = total_assets - total_liabilities

    if not all(math.isfinite(value) for value in [
        total_assets, total_liabilities, net_worth
    ]):
        return {
            "total_assets": 0,
            "total_liabilities": 0,
            "net_worth": 0,
            "status": "Invalid Input"
        }

    if net_worth > 0:
        status = "Positive Net Worth"
    elif net_worth < 0:
        status = "Negative Net Worth"
    else:
        status = "Zero Net Worth"

    return {
        "total_assets": round(total_assets, 2),
        "total_liabilities": round(total_liabilities, 2),
        "net_worth": round(net_worth, 2),
        "status": status
    }
