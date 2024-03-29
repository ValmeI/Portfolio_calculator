Korter1_Nimi = "Akadeemia 42-63"
#Korter2_Nimi = "Akadeemia 38-20"
Korter3_Nimi = "Vilde 90-193"
Korter4_Nimi = "Sõle 25B/3-21"

Korter1_Hind = 24500
#Korter2_Hind = 29900
Korter3_Hind = 29900

Korter1_Laen = 16708.64 #Algne laen 19600
#Korter2_Laen = 22146.08 #Algne laen 23920
Korter3_Laen = 17940.00
Korter4_Laen = 58500
Korterid = {Korter1_Nimi: Korter1_Hind}
LaenuSummad = {Korter1_Nimi: Korter1_Laen}


# Laenumakse kuus - Laenu summa, intress % na ja aastad
def apr_month(loan_sum, annual_interest_rate, years):
    rate = annual_interest_rate / 1200
    months = years * 12
    # Ülemine osa APR tehtest ja kuud on astmes'
    a = (loan_sum * rate * ((1 + rate) ** months))
    # Alumine osa tehtest ja kuud on astmes'
    b = (((1+rate)**months)-1)
    # tehte jagamine'
    monthly_payment = a/b

    return round(monthly_payment)


# Function that gives the balance - Laenu summa, intress %na, aastad ja number_of_payments made already kuudes
def apr_balance(principle, annual_interest_rate, duration, number_of_payments):
    rate = annual_interest_rate/1200
    months = duration*12
    a = ((1+rate)**months)
    b = ((1+rate)**number_of_payments)
    c = (((1+rate)**months)-1)
    if rate > 0:
        remaining_loan_balance = principle*((a-b)/c)
    #else:
        #remaining_loan_balance = principle*(1-(number_of_payments/n))
    return round(remaining_loan_balance)


# Total value of the property
def kinnisvara_vaartus():
    total_value = 0
    for k, v in Korterid.items():
        total_value += v
    return total_value
