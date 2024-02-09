import Aktsiad

MORR_EUR_STOCKS = {"EFT1T": 55,
                   "TKM1T": 53,
                   "TSM1T": 560,
                   "EXXT.DE": 52.014,
                   "SPYW.DE": 211.337	
                   }

# morr_usa_stocks = {}

# Sõle_Laen_Kuupäev = date(2011, 8, 25) #Müüdud 22.06.2021

VAL_CAPITAL_RAHA = 14260

LAHTSE_RAHA = 100370 # maha liita tasaarvestuse raha

m_aktsiad = round(Aktsiad.stocks_value_combined(stock_dictionary=MORR_EUR_STOCKS, org_currency=True))

MORR_RAHA = 14450

LHV_VOLAKIRI = 2402
BIGBANK_VOLAKIRI = 3221
INBANK_VOLAKIRI = 1101

kokku = round(VAL_CAPITAL_RAHA / 2 + MORR_RAHA + m_aktsiad + LAHTSE_RAHA / 2 + LHV_VOLAKIRI + BIGBANK_VOLAKIRI + INBANK_VOLAKIRI)
