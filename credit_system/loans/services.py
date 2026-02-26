# loans/services.py
import math

from datetime import date
from django.db.models import Sum

def calculate_emi(principal, annual_rate, tenure_months):
    r = annual_rate / (12 * 100)
    n = tenure_months

    if r == 0:
        return principal / n

    emi = (principal * r * math.pow(1 + r, n)) / (math.pow(1 + r, n) - 1)
    return round(emi, 2)


def calculate_credit_score(customer):
    loans = customer.loans.all()

    if not loans.exists():
        return 50  # neutral score

    # HARD FAIL
    if customer.current_debt > customer.approved_limit:
        return 0

    score = 0

    # 1. EMIs paid on time (40)
    total_emis = sum(l.tenure for l in loans)
    paid_on_time = sum(l.emis_paid_on_time for l in loans)

    if total_emis > 0:
        score += (paid_on_time / total_emis) * 40

    # 2. Number of loans (20)
    loan_count = loans.count()
    score += min(loan_count * 5, 20)

    # 3. Current year activity (20)
    current_year_loans = loans.filter(start_date__year=date.today().year).count()
    score += min(current_year_loans * 10, 20)

    # 4. Loan volume vs approved limit (20)
    total_loan_amount = loans.aggregate(
        Sum("loan_amount")
    )["loan_amount__sum"] or 0

    utilization = total_loan_amount / customer.approved_limit
    score += max(0, (1 - utilization) * 20)

    return int(score)

def check_loan_eligibility(customer, loan_amount, interest_rate, tenure):
    credit_score = calculate_credit_score(customer)

    emi = calculate_emi(loan_amount, interest_rate, tenure)

    # EMI load rule
    existing_emi_sum = sum(
        calculate_emi(l.loan_amount, l.interest_rate, l.tenure)
        for l in customer.loans.filter(is_active=True)
    )

    if existing_emi_sum + emi > 0.5 * customer.monthly_salary:
        return {
            "approved": False,
            "corrected_interest_rate": interest_rate,
            "monthly_installment": emi
        }

    corrected_rate = interest_rate
    approved = True

    if credit_score > 50:
        pass
    elif credit_score > 30:
        corrected_rate = max(interest_rate, 12)
    elif credit_score > 10:
        corrected_rate = max(interest_rate, 16)
    else:
        approved = False

    corrected_emi = calculate_emi(loan_amount, corrected_rate, tenure)

    return {
        "approved": approved,
        "credit_score": credit_score,
        "corrected_interest_rate": corrected_rate,
        "monthly_installment": corrected_emi
    }
