import Aktsiad

morr_eur_stocks = {"EFT1T": 55,
                   "TKM1T": 53,
                   "TSM1T": 560,
                   "EXXT": 42.434,
                   "SPYW": 184.498
                   }

'''morr_usa_stocks = {}'''

'''Sõle_Laen_Kuupäev = date(2011, 8, 25) #Müüdud 22.06.2021'''

ValCapitalRaha = 12260

Lähtse_Raha = 117382


m_aktsiad = round(Aktsiad.stocks_value_combined(stock_dictionary=morr_eur_stocks, org_currency=True))

m_raha = 0

kokku = round(ValCapitalRaha / 2 + m_raha + m_aktsiad + Lähtse_Raha / 2)
