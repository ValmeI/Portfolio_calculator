from datetime import date
from aktsiad import StockManager
import excel_functions
import functions as F
from . import morr


ignar_stocks_manager = StockManager("Ignar")


FYS_EUR_STOCKS = {"TKM1T": 355, "EFT1T": 113, "SXR8": 1.546}

FYS_USA_STOCKS = {}

JUR_USA_STOCKS = {
    "AAPL": 69,
    "AMD": 70,
    "MSFT": 14,
    "AMZN": 56,
    "GOOGL": 36,
    "BRK.B": 2,
}

JUR_EUR_STOCKS = {"IUSE": 119.8133, "EXXT": 56.8561}

BTC_AMOUNT = 0
ETH_AMOUNT = 0

ETH_EUR = ignar_stocks_manager.crypto_in_eur("Ethereum") * ETH_AMOUNT
Bitcoin_EUR = ignar_stocks_manager.crypto_in_eur("bitcoin") * BTC_AMOUNT

# Vanad ja refinants Akadeemia laenu kuupäevad yyyy.mm.dd'
# Vana_Aka42_63_Laen_Kuupäev = date(2016, 2, 16)
# Vana_Aka38_20_Laen_Kuupäev = date(2017, 5, 9)

# Aka42_63_Laen_Kuupäev = date(2018, 12, 5) # Välja ostetud 10.11.2023
# Aka38_20_Laen_Kuupäev = date(2018, 12, 5) # 28.10.2021 Müüdud
VILDE90_193_LAEN_KUUPAEV = date(2019, 4, 9)

# emale võlg 10k
FUSISIK_RAHA = -10000
FysIsikAktsaid = ignar_stocks_manager.stocks_value_combined(
    stock_dictionary=FYS_EUR_STOCKS, org_currency=True
)  # + ignar_stocks_manager.stocks_value_combined(stock_dictionary=FYS_USA_STOCKS, org_currency=False)

FysIsik = round(FUSISIK_RAHA + FysIsikAktsaid)

CLEVERON_AKTSIA = 4 * 150  # Ümber hinnatud 11.11.2023. Uus hind 150 EUR, vana koos clevoniga 1050 EUR tk
Juraktsiad = round(
    ignar_stocks_manager.stocks_value_combined(stock_dictionary=JUR_USA_STOCKS, org_currency=False)
    + ignar_stocks_manager.stocks_value_combined(stock_dictionary=JUR_EUR_STOCKS, org_currency=True)
    + CLEVERON_AKTSIA
)
Jur_Krypto = round(Bitcoin_EUR + ETH_EUR)

VOLAKIRJAD_KOKKU = 7508.80 + 9491.49 + 5000  # Everaus

# jur isiku raha LHV'
JUR_RAHA = 1000
JUR_FUNDERBEAM = 4400  # F.get_funderbeam_marketvalue() # 26.08.2023 Commented out because of Funderbeam added 2FA and market value does not change that often anymore
JUR_IB_RAHA = 200
JurIsik = round(
    JUR_RAHA + JUR_FUNDERBEAM + JUR_IB_RAHA + Juraktsiad + morr.VAL_CAPITAL_RAHA / 2 + Jur_Krypto + VOLAKIRJAD_KOKKU
)
# Mörr on väike karu'

# Raha ehk likviitsus,ka Krypto, jur ja fys kokku'
RahaKokku = round(FUSISIK_RAHA + JUR_RAHA + morr.VAL_CAPITAL_RAHA / 2 + JUR_IB_RAHA + Jur_Krypto)

# üür'
VILDE_ISA = 240
VILDE_LAEN = 175  # alates oktoobrist on tegelikult 163.35 EUR kuu
VILDE_KINDLUSTUS = 7.91
# ehk kuupäev millal arvutust tehakse
ARVUTAMISE_KP = 1

Uus_vilde_summa = F.vilde_calculation(
    input_day=ARVUTAMISE_KP,
    last_calculation_sum=excel_functions.get_last_row(excel_name="Portfell", column_number=9),
    new_sum_to_add=round(F.dividend_with_certain_date(VILDE_ISA) - VILDE_LAEN - VILDE_KINDLUSTUS, 2),
    last_input_excel_date=excel_functions.get_last_row(excel_name="Portfell", column_number=1),
)

Uus_vilde_summa = round(Uus_vilde_summa, 2)
