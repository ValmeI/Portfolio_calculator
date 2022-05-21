import Aktsiad


morr_eur_stocks = {"APG1L": 196,
                   "EFT1T": 55,
                   "TKM1T": 53,
                   "TSM1T": 560,
                   "EXS1": 0.013,
                   "EXSA": 0.069,
                   "EXXT": 34.289,
                   "SPYD": 70.482,
                   "SPYW": 161.400
                   }

'''morr_usa_stocks = {}'''

'''Sõle_Laen_Kuupäev = date(2011, 8, 25) #Müüdud 22.06.2021'''

ValCapitalRaha = 11000

Lähtse_Raha = 100000

m_aktsiad = round(Aktsiad.stocks_value_combined(morr_eur_stocks, True))

m_raha = 223

kokku = round(ValCapitalRaha/2 + m_raha + m_aktsiad + Lähtse_Raha/2)
