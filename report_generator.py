
import os
import math
from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch


def generate_financial_report(income, expenses, savings, savings_rate, categories):

    try:
        income = float(income)
        expenses = float(expenses)
        savings = float(savings)
        savings_rate = float(savings_rate)

    except (TypeError, ValueError):
        raise ValueError("Invalid financial values.")

    if not all(math.isfinite(value) for value in [
        income, expenses, savings, savings_rate
    ]):
        raise ValueError("Financial values must be finite numbers.")

    if income < 0 or expenses < 0:
        raise ValueError("Income and expenses cannot be negative.")

    if not isinstance(categories, dict):
        raise ValueError("Categories must be provided as a dictionary.")

    validated_categories = {}

    for category, amount in categories.items():

        if not isinstance(category, str) or not category.strip():
            raise ValueError("Invalid category name.")

        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValueError("Invalid category expense amount.")

        if not math.isfinite(amount) or amount < 0:
            raise ValueError("Category expenses must be valid non-negative numbers.")

        validated_categories[category] = amount

    os.makedirs("reports", exist_ok=True)

    filename = "reports/FinWise_Financial_Report.pdf"

    pdf = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - inch

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, y, "FinWise AI Financial Report")

    y -= 35
    pdf.setFont("Helvetica", 10)
    pdf.drawString(
        50, y,
        f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}"
    )

    y -= 50
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Financial Summary")

    y -= 30
    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, y, f"Total Income: Rs. {income:,.2f}")
    y -= 25

    pdf.drawString(50, y, f"Total Expenses: Rs. {expenses:,.2f}")
    y -= 25

    pdf.drawString(50, y, f"Total Savings: Rs. {savings:,.2f}")
    y -= 25

    pdf.drawString(50, y, f"Savings Rate: {savings_rate:.2f}%")

    y -= 50
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Category-wise Expenses")

    y -= 30
    pdf.setFont("Helvetica", 11)

    for category, amount in validated_categories.items():

        if y < 60:
            pdf.showPage()
            y = height - inch
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(50, y, "Category-wise Expenses (Continued)")
            y -= 35
            pdf.setFont("Helvetica", 11)

        pdf.drawString(60, y, f"{category}: Rs. {amount:,.2f}")
        y -= 22

    pdf.save()

    return filename
