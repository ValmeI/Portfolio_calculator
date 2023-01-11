import Aktsiad

morr_eur_stocks = {"APG1L": 196,
                   "EFT1T": 55,
                   "TKM1T": 53,
                   "TSM1T": 560,
                   "EXS1": 0.013,
                   "EXSA.DE": 0.069,
                   "EXXT": 41.550,
                   "SPYD": 83.178,
                   "SPYW": 182.277
                   }

'''morr_usa_stocks = {}'''

'''Sõle_Laen_Kuupäev = date(2011, 8, 25) #Müüdud 22.06.2021'''

ValCapitalRaha = 11980

Lähtse_Raha = 103033

m_aktsiad = round(Aktsiad.stocks_value_combined(stock_dictionary=morr_eur_stocks, org_currency=True))

m_raha = 174.42

kokku = round(ValCapitalRaha / 2 + m_raha + m_aktsiad + Lähtse_Raha / 2)
