from aktsiad import StockManager

MORR_EUR_STOCKS = {"EFT1T": 55, "TKM1T": 563, "TSM1T": 560, "EXXT": 99.584, "SPYW": 354.490}

# morr_usa_stocks = {}
# Sõle_Laen_Kuupäev = date(2011, 8, 25) #Müüdud 22.06.2021

VAL_CAPITAL_RAHA = 22000

TAHTAJALINE_HOIUS = 0

# TODO: move lot of those variables to config env file
# Lähtse väärtuse arvutus, staatiline
LAHTSE_LAENUJAAK = 260000  # 5.05.2025 seisuga
LAHTSE_HINDAMISAKTI_VAARTUS = 386000  # 29.04.2025 seisuga
LAHTSE_ARVUTUSLIK_VAARTUS = round(LAHTSE_HINDAMISAKTI_VAARTUS - LAHTSE_LAENUJAAK)

margit_stocks_manager = StockManager("Margit")

m_aktsiad = round(margit_stocks_manager.stocks_value_combined(stock_dictionary=MORR_EUR_STOCKS, org_currency=True))

MORR_RAHA = 11123

VOLAKIRJAD_KOKKU = 14782.86

kokku = round(VAL_CAPITAL_RAHA / 2 + MORR_RAHA + m_aktsiad + LAHTSE_ARVUTUSLIK_VAARTUS / 2 + VOLAKIRJAD_KOKKU)
