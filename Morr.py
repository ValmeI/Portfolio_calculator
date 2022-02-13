import Aktsiad


morr_eur_stocks = {"APG1L": 196,
                   "EFT1T": 55,
                   "TKM1T": 53,
                   "TSM1T": 560,
                   "EXS1": 14.302,
                   "EXSA": 81.123,
                   "EXXT": 30.557,
                   "SPYD": 63.540,
                   "SPYW": 240.985
                   }

'''morr_usa_stocks = {}'''

'''Sõle_Laen_Kuupäev = date(2011, 8, 25) #Müüdud 22.06.2021'''

ValCapitalRaha = 10500

Lähtse_Raha = 20000

m_aktsiad = round(Aktsiad.stocks_value_combined(morr_eur_stocks, True))

m_raha = 32572.51

kokku = round(ValCapitalRaha/2 + m_raha + m_aktsiad + Lähtse_Raha/2)
