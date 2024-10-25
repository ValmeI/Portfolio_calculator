Korter1_Nimi = "Akadeemia 42-63"
# Korter2_Nimi = "Akadeemia 38-20"
Korter3_Nimi = "Vilde 90-193"
# Korter4_Nimi = "Sõle 25B/3-21"

Korter1_Hind = 24500
# Korter2_Hind = 29900
Korter3_Hind = 29900

Korter1_Laen = 16708.64  # Algne laen 19600
# Korter2_Laen = 22146.08 # Algne laen 23920
Korter3_Laen = 17940.00
# Korter4_Laen = 58500

APARTMENTS = {Korter1_Nimi: Korter1_Hind}


def apr_month(loan_sum: float, annual_interest_rate: float, years: int) -> int:
    rate = annual_interest_rate / 1200
    months = years * 12
    a = loan_sum * rate * ((1 + rate) ** months)
    b = ((1 + rate) ** months) - 1
    monthly_payment = a / b
    return round(monthly_payment)


def apr_balance(principle: float, annual_interest_rate: float, duration: int, number_of_payments: int) -> float:
    remaining_loan_balance = 0
    rate = annual_interest_rate / 1200
    months = duration * 12
    a = (1 + rate) ** months
    b = (1 + rate) ** number_of_payments
    c = ((1 + rate) ** months) - 1
    if rate > 0:
        remaining_loan_balance = principle * ((a - b) / c)
    return round(remaining_loan_balance)


def calculate_real_estate_total_value() -> int:
    return sum(v for v in APARTMENTS.values())
