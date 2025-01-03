from datetime import date
from Aktsiad import StockManager
import Excel_functions
import Functions as F
import Morr
from Functions import what_path_for_file


ignar_stocks_manager = StockManager("Ignar")

path = what_path_for_file()

FYS_EUR_STOCKS = {"TKM1T.TL": 355, "EFT1T.TL": 113, "SXR8.DE": 1.199}

FYS_USA_STOCKS = {"SXR8.DE": 1.233}

JUR_USA_STOCKS = {
    "AAPL": 69,
    "TSLA": 15,
    "AMD": 70,
    "QCOM": 24.9907,
    "MSFT": 14,
    "AMZN": 56,
    "GOOGL": 36,
    "NIO": 93,
    "XPEV": 72,
    "NKE": 11,
    "INTC": 25,
    "SNOW": 6,
    "BRK.B": 2,
}

JUR_EUR_STOCKS = {"IUSE.ETF": 99.7312}

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
) + ignar_stocks_manager.stocks_value_combined(stock_dictionary=FYS_USA_STOCKS, org_currency=False)

FysIsik = round(FUSISIK_RAHA + FysIsikAktsaid)

CLEVERON_AKTSIA = 4 * 150  # Ümber hinnatud 11.11.2023. Uus hind 150 EUR, vana koos clevoniga 1050 EUR tk
JurAktsiad = round(
    ignar_stocks_manager.stocks_value_combined(stock_dictionary=JUR_USA_STOCKS, org_currency=False)
    + ignar_stocks_manager.stocks_value_combined(stock_dictionary=JUR_EUR_STOCKS, org_currency=True)
    + CLEVERON_AKTSIA
)
Jur_Krypto = round(Bitcoin_EUR + ETH_EUR)

VOLAKIRJAD_KOKKU = 7508.80 + 9491.49

# jur isiku raha LHV'
JUR_RAHA = 2800
JUR_FUNDERBEAM = 4400  # F.get_funderbeam_marketvalue() # 26.08.2023 Commented out because of Funderbeam added 2FA and market value does not change that often anymore
JUR_IB_RAHA = -3340
JurIsik = round(
    JUR_RAHA + JUR_FUNDERBEAM + JUR_IB_RAHA + JurAktsiad + Morr.VAL_CAPITAL_RAHA / 2 + Jur_Krypto + VOLAKIRJAD_KOKKU
)
# Mörr on väike karu'

# Raha ehk likviitsus,ka Krypto, jur ja fys kokku'
RahaKokku = round(FUSISIK_RAHA + JUR_RAHA + Morr.VAL_CAPITAL_RAHA / 2 + JUR_IB_RAHA + Jur_Krypto)

# üür'
VILDE_ISA = 240
VILDE_LAEN = 175  # alates oktoobrist on tegelikult 163.35 EUR kuu
VILDE_KINDLUSTUS = 7.91
# ehk kuupäev millal arvutust tehakse
ARVUTAMISE_KP = 1

Uus_vilde_summa = F.vilde_calculation(
    input_day=ARVUTAMISE_KP,
    last_calculation_sum=Excel_functions.get_last_row(excel_name="Portfell", column_number=9),
    new_sum_to_add=round(F.dividend_with_certain_date(VILDE_ISA) - VILDE_LAEN - VILDE_KINDLUSTUS, 2),
    last_input_excel_date=Excel_functions.get_last_row(excel_name="Portfell", column_number=1),
)

Uus_vilde_summa = round(Uus_vilde_summa, 2)
