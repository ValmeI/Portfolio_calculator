from Aktsiad import StockManager

MORR_EUR_STOCKS = {"EFT1T.TL": 55, "TKM1T.TL": 563, "TSM1T.TL": 560, "EXXT.DE": 74.655, "SPYW.DE": 281.380}

# morr_usa_stocks = {}

# Sõle_Laen_Kuupäev = date(2011, 8, 25) #Müüdud 22.06.2021

VAL_CAPITAL_RAHA = 3692 + 16536

TAHTAJALINE_HOIUS = 4143.93

# Lähtse väärtuse arvutus, staatiline
LAHTSE_OMAFINANTSEERING = 53370  # 25.10.2024 seisuga
LAHTSE_ARVUTUSLIK_VAARTUS_KASUTUS_KOKKU = 246338  # 25.10.2024 seisuga
LAHTSE_HINDAMISAKTI_VAARTUS = 316000  # 3.10.2024 seisuga
LAHTSE_ARVUTUSLIK_VAARTUS = round(
    LAHTSE_HINDAMISAKTI_VAARTUS - LAHTSE_ARVUTUSLIK_VAARTUS_KASUTUS_KOKKU + LAHTSE_OMAFINANTSEERING
)

margit_stocks_manager = StockManager("Margit")

m_aktsiad = round(margit_stocks_manager.stocks_value_combined(stock_dictionary=MORR_EUR_STOCKS, org_currency=True))

MORR_RAHA = 9106

VOLAKIRJAD_KOKKU = 14782.86


kokku = round(VAL_CAPITAL_RAHA / 2 + MORR_RAHA + m_aktsiad + LAHTSE_ARVUTUSLIK_VAARTUS / 2 + VOLAKIRJAD_KOKKU)
