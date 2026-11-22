
import math


def analyze_credit_score(score):

    try:
        score = float(score)
    except (TypeError, ValueError):
        return {
            "rating": "Invalid Score",
            "recommendation": "Enter a valid credit score between 300 and 900."
        }

    if not math.isfinite(score) or not score.is_integer():
        return {
            "rating": "Invalid Score",
            "recommendation": "Enter a valid whole-number credit score between 300 and 900."
        }

    if score < 300 or score > 900:
        return {
            "rating": "Invalid Score",
            "recommendation": "Enter a score between 300 and 900."
        }

    if score < 650:
        rating = "Poor"
        recommendation = "Pay your EMIs and credit card bills on time. Reduce outstanding debt."

    elif score < 700:
        rating = "Fair"
        recommendation = "Maintain timely payments and avoid applying for too many loans."

    elif score < 750:
        rating = "Good"
        recommendation = "Continue paying bills on time and keep credit utilization low."

    elif score < 800:
        rating = "Very Good"
        recommendation = "Maintain your repayment history and avoid unnecessary credit applications."

    else:
        rating = "Excellent"
        recommendation = "Maintain your responsible credit habits."

    return {
        "rating": rating,
        "recommendation": recommendation
    }
