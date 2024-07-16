import Aktsiad

MORR_EUR_STOCKS = {"EFT1T": 55, "TKM1T": 563, "TSM1T": 560, "EXXT.DE": 58.941, "SPYW.DE": 232.141}

# morr_usa_stocks = {}

# Sõle_Laen_Kuupäev = date(2011, 8, 25) #Müüdud 22.06.2021

VAL_CAPITAL_RAHA = 17500

TAHTAJALINE_HOIUS = 4000

LAHTSE_RAHA = 55370  # maha liita tasaarvestuse raha

m_aktsiad = round(Aktsiad.stocks_value_combined(stock_dictionary=MORR_EUR_STOCKS, org_currency=True))

MORR_RAHA = 8900

LHV_VOLAKIRI = 2400
BIGBANK_VOLAKIRI = 6200
INBANK_VOLAKIRI = 1000
HOLM_VOLAKIRI = 1100
LIVEN_VOLAKIRI = 2100


kokku = round(
    VAL_CAPITAL_RAHA / 2 + MORR_RAHA + m_aktsiad + LAHTSE_RAHA / 2 + LHV_VOLAKIRI + BIGBANK_VOLAKIRI + INBANK_VOLAKIRI
)
